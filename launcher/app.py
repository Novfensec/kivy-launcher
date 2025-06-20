# -*- coding: utf-8 -*-
import os
import sys
import traceback
import logging
from glob import glob
from datetime import datetime
from os.path import dirname, join, exists, expanduser, realpath

from kivy.app import App
from kivy.lang import Builder
from kivy.utils import platform
from kivy.properties import ListProperty, BooleanProperty

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Launcher')

class Launcher(App):
    paths = ListProperty()
    logs = ListProperty()
    display_logs = BooleanProperty(False)

    def log(self, message, level='info'):
        """Improved logging with timestamp and levels"""
        timestamp = datetime.now().strftime('%X.%f')
        log_entry = f"{timestamp}: {message}"
        
        # Add to UI logs
        self.logs.append(log_entry)
        
        # Send to appropriate logger
        getattr(logger, level)(message)

    def build(self):
        self.log("Launcher started")
        self._request_permissions()
        self._setup_paths()
        self.root = Builder.load_file("launcher/app.kv")
        self.refresh_entries()
        return self.root

    def _setup_paths(self):
        """Configure search paths based on environment and platform"""
        if env_paths := os.environ.get("KIVYLAUNCHER_PATHS"):
            self.paths.extend(env_paths.split(","))
        elif platform == 'android':
            from jnius import autoclass
            Environment = autoclass('android.os.Environment')
            sdcard_path = Environment.getExternalStorageDirectory().getAbsolutePath()
            self.paths = [join(sdcard_path, "kivy")]
        else:
            self.paths = [expanduser("~/kivy")]

    def _request_permissions(self):
        """Request Android permissions if needed"""
        if platform == 'android':
            from android.permissions import request_permissions, Permission # type: ignore
            request_permissions([Permission.READ_EXTERNAL_STORAGE])

    def refresh_entries(self):
        """Scan and display available entries"""
        self.log("Refreshing entries")
        entries = []

        for entry in self.find_entries():
            entries.append({
                "data_title": entry.get("title", "Untitled App"),
                "data_path": entry.get("path"),
                "data_logo": entry.get("logo", "data/logo/kivy-icon-64.png"),
                "data_orientation": entry.get("orientation", ""),
                "data_author": entry.get("author", "Kivy"),
                "data_entry": entry
            })

        self.root.ids.rv.data = entries
        self.log(f"Found {len(entries)} entries")

    def find_entries(self):
        """Generator to find all valid entries in configured paths"""
        for path in self.paths:
            if not exists(path):
                self.log(f"Path not found: {path}", 'warning')
                continue
                
            self.log(f"Scanning: {path}")
            for filename in glob(join(path, "*", "android.txt")):
                if entry := self.read_entry(filename):
                    yield entry

    def read_entry(self, filename):
        """Parse an android.txt entry file"""
        self.log(f"Reading entry: {filename}")
        try:
            with open(filename, "r") as fd:
                data = {}
                for line in fd:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        data[key.strip()] = value.strip()
                
                if not data.get('title'):
                    self.log(f"Missing title in {filename}", 'warning')
                    return None
                
                # Add derived paths
                entry_dir = dirname(filename)
                data.update({
                    "entrypoint": realpath(join(entry_dir, "main.py")),
                    "path": entry_dir,
                    "logo": realpath(join(entry_dir, "icon.png")) 
                            if exists(join(entry_dir, "icon.png")) 
                            else "data/logo/kivy-icon-64.png"
                })
                return data
                
        except Exception as e:
            self.log(f"Error reading {filename}: {str(e)}", 'error')
            traceback.print_exc()
            return None

    def start_activity(self, entry):
        """Launch selected entry with platform-specific method"""
        if platform == "android":
            self._start_android_activity(entry)
        else:
            self._start_desktop_activity(entry)

    def _start_desktop_activity(self, entry):
        """Launch entry on desktop"""
        self.log(f"Launching desktop app: {entry['title']}")
        env = os.environ.copy()
        env["KIVYLAUNCHER_ENTRYPOINT"] = entry["entrypoint"]

        # Use current interpreter
        main_script = realpath(join(dirname(__file__), "..", "main.py"))
        try:
            process = __import__('subprocess').run( # nosec
                [sys.executable, main_script],
                env=env,
                shell=True,
                cwd=entry.get("path")
            )
        except Exception as e:
            self.log(f"Failed to launch: {str(e)}", 'error')

    def _start_android_activity(self, entry):
        """Launch entry on Android using JNI"""
        self.log(f"Starting Android activity: {entry['title']}")
        try:
            from jnius import autoclass
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            LauncherActivity = autoclass("org.launcher.android.LauncherActivity")
            Intent = autoclass("android.content.Intent")
            String = autoclass("java.lang.String")

            intent = Intent(PythonActivity.mActivity, LauncherActivity)
            intent.putExtra("entrypoint", String(entry["entrypoint"]))
            intent.putExtra("orientation", String(entry.get("orientation", "")))

            PythonActivity.mActivity.startActivity(intent)
        except Exception as e:
            self.log(f"Android launch failed: {str(e)}", 'error')
            traceback.print_exc()
