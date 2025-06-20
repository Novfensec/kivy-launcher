package org.launcher.android;

import android.util.Log;
import org.kivy.android.PythonActivity;

public class LauncherActivity extends PythonActivity {
    private static final String TAG = "LauncherActivity";

    @Override
    public void onBackPressed() {
        // Optionally finish this activity
        super.onBackPressed();

        // Start the main activity
        Intent intent = new Intent(this, org.kivy.android.PythonActivity.class);

        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP);
        startActivity(intent);
    }

}