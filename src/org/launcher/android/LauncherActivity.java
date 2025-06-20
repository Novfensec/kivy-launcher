package org.launcher.android;

import android.util.Log;
import org.kivy.android.PythonActivity;

public class LauncherActivity extends PythonActivity {
    private static final String TAG = "LauncherActivity";

    @Override
    public void onBackPressed() {
        Log.i(TAG, "Back button pressed");

        // Call PythonActivity's custom handler
        if (this instanceof PythonActivity) {
            ((PythonActivity) this).handleBackPressed();
            return;
        }

        super.onBackPressed();
    }
}