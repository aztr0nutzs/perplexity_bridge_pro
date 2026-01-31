package ai.perplexity.bridge;

import org.junit.Test;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

public class WebAppConfigTest {
    @Test
    public void isAllowedPage_allowsIndex() {
        assertTrue(WebAppConfig.isAllowedPage("index.html"));
    }

    @Test
    public void isAllowedPage_blocksUnknown() {
        assertFalse(WebAppConfig.isAllowedPage("unknown.html"));
    }
}
