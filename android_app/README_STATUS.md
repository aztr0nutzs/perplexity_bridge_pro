# ✅ ANDROID APP STATUS

## Current Status: FUNCTIONAL (WITH DEPENDENCIES)

The Android app is a WebView shell that loads the bundled UI from
`app/src/main/assets/www/index.html` and can connect to a bridge server
for chat, models, and project tooling.

## Corrections Applied

1. **Asset Path Alignment** ✅
   - WebView loads `assets/www/index.html` via `appassets.androidplatform.net`.
   - UI asset references now use relative paths so images resolve from `assets/www/assets/`.

2. **Production Package Name** ✅
   - Updated to `ai.perplexity.bridge` in manifest, applicationId, namespace, and source tree.

3. **APK Size Control** ✅
   - Trimmed the embedded project manifest so the APK does not ship large node_modules lists.
   - Android assets now include only the runtime UI and images.

4. **Version Info** ✅
   - `versionCode` and `versionName` are present in `app/build.gradle`.

5. **Activity Exported** ✅
   - The launcher activity remains `exported="true"` (required for launcher intent filters
     on Android 12+). This is expected and documented.

6. **Proguard/R8** ✅
   - Release builds now enable minification and resource shrinking with a
     `proguard-rules.pro` configuration.

## What Works

✅ WebView loads local UI assets
✅ Swipe-to-refresh reload
✅ Back navigation within WebView
✅ Basic WebView security hardening (file access disabled)
✅ R8 enabled for release builds

## What Requires a Backend

The UI expects a bridge server that implements the following endpoints:

- `GET /health`
- `GET /models`
- `POST /v1/chat/completions`
- `POST /terminal`
- `GET /project/file?path=...`
- `WS /ws/chat?api_key=...`

Without that server, the chat/editor/terminal features will not function.

## Build Steps

```bash
cd android_app

# Clean build
./gradlew clean

# Build debug APK
./gradlew assembleDebug

# Install on device
adb install app/build/outputs/apk/debug/app-debug.apk
```

## Testing Checklist

- [ ] App installs without errors
- [ ] WebView loads content
- [ ] No 404 errors in logcat
- [ ] Swipe-to-refresh works
- [ ] Back button navigation works
- [ ] APK size is reasonable (<20MB)

---

**Last Updated:** 2026-01-19
