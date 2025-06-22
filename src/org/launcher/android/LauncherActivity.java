package org.launcher.android;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;

import org.kivy.android.PythonActivity;

public class LauncherActivity extends PythonActivity {
    private static final String TAG = "LauncherActivity";

    @Override
    public boolean dispatchKeyEvent(KeyEvent event) {
        int keyCode = event.getKeyCode();
        Log.d(TAG, "dispatchKeyEvent: " + keyCode);

        if (keyCode == KeyEvent.KEYCODE_BACK && event.getAction() == KeyEvent.ACTION_DOWN) {
            Log.d(TAG, "BACK key intercepted!");
            finish();  // Handle back press or communicate with Python if needed
            return true;
        }

        return super.dispatchKeyEvent(event);
    }
}