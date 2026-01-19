# ⚠️ ANDROID APP STATUS - WORK IN PROGRESS

## Current Status: INCOMPLETE

The Android app in this directory is **NOT FUNCTIONAL** in its current state.

### Issues That Must Be Fixed:

1. **Wrong Asset Path** 🔴 CRITICAL
   - WebAppConfig.java expects: `assets/www/index.html`
   - Actual location: `assets/perplexity_api_project_files/ui/perplex_index2.html`
   - **Fix Required:** Restructure assets OR update paths

2. **BioGameBridge Non-Functional** 🔴 CRITICAL
   - All JavaScript bridge methods are stubs
   - Methods: playKNXT4(), openStore(), loadLobby(), closeGame()
   - **Fix Required:** Implement actual functionality or remove

3. **Example Package Name** 🔴 CRITICAL
   - Current: `com.example.perplexitybridge`
   - **Fix Required:** Change to production package name

4. **Massive APK Size** 🔴 CRITICAL
   - Assets include full node_modules (~800 files)
   - Expected APK size: >50MB
   - **Fix Required:** Remove node_modules, only include runtime files

5. **No Version Info** 🟡 MEDIUM
   - No versionCode or versionName in build.gradle
   - **Fix Required:** Add version information

6. **Activity Exported True** 🟡 MEDIUM
   - Security concern: Other apps can launch activity
   - **Fix Required:** Set to false or document why true

7. **No Proguard/R8** 🟡 MEDIUM
   - No code shrinking or obfuscation
   - **Fix Required:** Enable R8 with proper rules

## What Works:

✅ Basic WebView setup  
✅ Security settings (file access disabled)  
✅ Swipe-to-refresh functionality  
✅ Modern AndroidX libraries  

## To Make This Work:

### Option 1: Fix Asset Structure (Recommended)

1. Create `app/src/main/assets/www/` directory
2. Copy only these files:
   ```
   www/
   ├── index.html (rename from perplex_index2.html)
   └── (any other runtime files needed)
   ```
3. Update references in index.html
4. Test loading in WebView

### Option 2: Update Paths

1. Edit `WebAppConfig.java`:
   ```java
   public static final String BASE_URL = 
       "https://appassets.androidplatform.net/assets/perplexity_api_project_files/ui/";
   public static final String[] ALLOWED_PAGES = { 
       "perplex_index2.html" 
   };
   ```
2. Edit `MainActivity.java` line 82:
   ```java
   webView.loadUrl("https://appassets.androidplatform.net/assets/perplexity_api_project_files/ui/perplex_index2.html");
   ```

### Option 3: Use External URL

1. Point WebView to running bridge server:
   ```java
   webView.loadUrl("http://your-server:7860/");
   ```
2. Handle network connectivity
3. Add error states for offline mode

## Package Name Change

1. Refactor package in Android Studio:
   - Right-click package → Refactor → Rename
   - Choose "Rename package"
2. Or manually:
   - Update AndroidManifest.xml
   - Update all Java file package declarations
   - Update directory structure

## Build Steps (Once Fixed):

```bash
cd android_app

# Clean build
./gradlew clean

# Build debug APK
./gradlew assembleDebug

# Install on device
adb install app/build/outputs/apk/debug/app-debug.apk
```

## Testing Checklist:

- [ ] App installs without errors
- [ ] WebView loads content
- [ ] No 404 errors in logcat
- [ ] JavaScript bridge works (if implemented)
- [ ] Swipe-to-refresh works
- [ ] Back button navigation works
- [ ] APK size is reasonable (<20MB)

## Current Build Status: ⛔ WILL NOT RUN

**Do not attempt to install this app without fixing the above issues first.**

## Need Help?

See the main inspection report: `PHASE_0-9_INSPECTION_REPORT.md` (Phase 9)

---

**Last Updated:** 2026-01-19  
**Status:** Requires significant work before functional
