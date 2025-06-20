# -*- coding: utf-8 -*-

import os
import sys
import traceback

def run_entrypoint(entrypoint):
    """Run a Python script at the given entrypoint."""
    import runpy
    entrypoint_path = os.path.dirname(os.path.abspath(entrypoint))
    if entrypoint_path not in sys.path:
        sys.path.append(entrypoint_path)
    try:
        runpy.run_path(entrypoint, run_name="__main__")
    except Exception:
        print("Error running entrypoint:", entrypoint)
        traceback.print_exc()

def run_launcher():
    """Run the main launcher app."""
    from launcher.app import Launcher
    Launcher().run()

def dispatch():
    """Dispatch to entrypoint or launcher depending on environment."""
    entrypoint = os.environ.get("KIVYLAUNCHER_ENTRYPOINT")
    if entrypoint:
        print("Launching entrypoint:", entrypoint)
        run_entrypoint(entrypoint)
        return

    # Try Android intent-based launch
    try:
        from jnius import autoclass
        activity = autoclass("org.kivy.android.LauncherActivity").mActivity
        intent = activity.getIntent()
        entrypoint = intent.getStringExtra("entrypoint")
        orientation = intent.getStringExtra("orientation")

        if orientation:
            # Set screen orientation if specified
            orientation_map = {
                "portrait": 0x1,   # SCREEN_ORIENTATION_PORTRAIT
                "landscape": 0x0,  # SCREEN_ORIENTATION_LANDSCAPE
                "sensor": 0x4      # SCREEN_ORIENTATION_SENSOR
            }
            value = orientation_map.get(orientation.lower())
            if value is not None:
                activity.setRequestedOrientation(value)

        if entrypoint:
            print("Launching Android entrypoint:", entrypoint)
            run_entrypoint(entrypoint)
            return
    except Exception:
        print("Android intent dispatch failed, falling back to launcher.")
        traceback.print_exc()

    # Fallback: run the launcher itself
    run_launcher()

if __name__ == "__main__":
    dispatch()
