package org.launcher.android;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;

import org.kivy.android.PythonActivity;

public class LauncherActivity extends PythonActivity {
    private static final String TAG = "LauncherActivity";

    @Override
    public boolean dispatchKeyEvent(KeyEvent event) {
        int keyCode = event.getKeyCode();
        Log.d(TAG, "dispatchKeyEvent: " + keyCode);

        if (keyCode == KeyEvent.KEYCODE_BACK && event.getAction() == KeyEvent.ACTION_DOWN) {
            Log.d(TAG, "BACK key intercepted!");
            finish();  // or send to Python
            return true;  // Consume the event
        }

        // For all other keys, let SDL handle it
        return super.dispatchKeyEvent(event);
    }
}