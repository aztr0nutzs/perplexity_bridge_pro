# Project-specific ProGuard/R8 rules.
# Keep WebView-related classes (defensive; most are already kept by default).
-keep class android.webkit.** { *; }
-keepclassmembers class android.webkit.** { *; }
