package com.example.perplexitybridge;

import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

public final class WebAppConfig {
    static final String BASE_URL = "https://appassets.androidplatform.net/assets/www/";
    private static final Set<String> ALLOWED_PAGES;

    static {
        Set<String> allowed = new HashSet<>();
        allowed.add("index.html");
        ALLOWED_PAGES = Collections.unmodifiableSet(allowed);
    }

    private WebAppConfig() {
    }

    static boolean isAllowedPage(String fileName) {
        return ALLOWED_PAGES.contains(fileName);
    }
}
