package org.launcher.android;

import android.content.Intent;
import android.util.Log;

import org.kivy.android.PythonActivity;

public class LauncherActivity extends PythonActivity {
    private static final String TAG = "LauncherActivity";

    @Override
    public void onBackPressed() {
        super.onBackPressed();

        Intent intent = new Intent(this, org.kivy.android.PythonActivity.class);
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP);
        startActivity(intent);
    }
}