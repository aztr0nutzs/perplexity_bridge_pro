package com.example.perplexitybridge;

import android.util.Log;
import android.webkit.JavascriptInterface;

public class BioGameBridge {
    private static final String TAG = "PerplexityBridge";
    private final MainActivity activity;

    public BioGameBridge(MainActivity activity) {
        this.activity = activity;
    }

    @JavascriptInterface
    public void playKNXT4(String params) {
        Log.d(TAG, "playKNXT4() called with params: " + params);
        activity.runOnUiThread(() -> activity.loadLocalPage("index.html"));
    }

    @JavascriptInterface
    public void openStore(String params) {
        Log.d(TAG, "openStore() called with params: " + params);
        activity.runOnUiThread(() -> activity.loadLocalPage("index.html"));
    }

    @JavascriptInterface
    public void loadLobby() {
        Log.d(TAG, "loadLobby() called");
        activity.runOnUiThread(() -> activity.loadLocalPage("index.html"));
    }

    @JavascriptInterface
    public void closeGame() {
        Log.d(TAG, "closeGame() called");
    }
}
