# Perplexity Bridge Pro - Project Roadmap

## Executive Summary

This project is a FastAPI bridge service that proxies requests to Perplexity AI API, with a web UI and VSCode extension. The codebase has several **critical issues** that prevent it from working correctly in production.

---

## 🔴 CRITICAL ISSUES (Must Fix Immediately)

### 1. **Rate Limiter Not Integrated**
- **Problem**: `slowapi` limiter is set on `app.state` but middleware is missing
- **Location**: `app.py` line 9, `rate_limit.py`
- **Impact**: Rate limiting will not work, causing potential API abuse
- **Fix**: Add `slowapi.errors.RateLimitExceeded` exception handler and ensure limiter is properly initialized

### 2. **Missing CORS Configuration**
- **Problem**: No CORS middleware configured
- **Location**: `app.py`
- **Impact**: Browser UI cannot make requests to the API (CORS errors)
- **Fix**: Add `CORSMiddleware` from `fastapi.middleware.cors`

### 3. **No Error Handling**
- **Problem**: No try/except blocks anywhere
- **Location**: `app.py` (lines 28-36, 38-50), `adapters/roo_adapter.py`
- **Impact**: Any API failure will crash the application
- **Fix**: Add comprehensive error handling with proper HTTP status codes

### 4. **WebSocket Authentication Missing**
- **Problem**: `/ws/chat` endpoint accepts connections without authentication
- **Location**: `app.py` line 38
- **Impact**: Unauthorized access to WebSocket endpoint
- **Fix**: Add authentication check before accepting WebSocket connection

### 5. **Configuration Validation Missing**
- **Problem**: No check if `PERPLEXITY_API_KEY` exists before starting
- **Location**: `config.py`
- **Impact**: Application starts but fails silently on first request
- **Fix**: Add validation that raises error if required env vars are missing

---

## 🟠 HIGH PRIORITY (Fix Soon)

### 6. **UI Configuration Not Persisted**
- **Problem**: Settings saved with `alert()` but not stored
- **Location**: `ui/app.js` line 7
- **Impact**: Users must re-enter configuration on every page load
- **Fix**: Use `localStorage.setItem()` and load on page load

### 7. **UI Missing WebSocket Support**
- **Problem**: WebSocket endpoint exists but UI only uses REST
- **Location**: `ui/app.js`
- **Impact**: No streaming capabilities in UI
- **Fix**: Add WebSocket client implementation for streaming responses

### 8. **VSCode Extension Missing Dependencies**
- **Problem**: `axios` used but not in `package.json`
- **Location**: `vscode_extension/package.json`, `extension.js`
- **Impact**: Extension won't install/run correctly
- **Fix**: Add `axios` to dependencies

### 9. **VSCode Extension Hardcoded Configuration**
- **Problem**: URL and API key hardcoded in code
- **Location**: `vscode_extension/extension.js` line 8, 11
- **Impact**: Cannot configure different environments
- **Fix**: Add VSCode configuration settings schema

### 10. **API Response Validation Missing**
- **Problem**: Directly accesses `r.json()` without checking structure
- **Location**: `app.py` line 36, `adapters/roo_adapter.py` line 13
- **Impact**: Will crash if Perplexity API returns unexpected format
- **Fix**: Add response validation and error handling

### 11. **No Health Check Endpoint**
- **Problem**: No way to check if service is running
- **Location**: `app.py`
- **Impact**: Difficult to monitor/debug service status
- **Fix**: Add `/health` or `/` endpoint returning service status

---

## 🟡 MEDIUM PRIORITY (Nice to Have)

### 12. **Input Validation Weak**
- **Problem**: Pydantic models lack strict validation (e.g., `messages:list` should validate structure)
- **Location**: `app.py` lines 11-17
- **Fix**: Add detailed Pydantic validation with custom validators

### 13. **No Logging**
- **Problem**: No logging infrastructure
- **Location**: Throughout codebase
- **Fix**: Add structured logging with appropriate log levels

### 14. **UI Lacks Loading/Error States**
- **Problem**: No visual feedback during requests or errors
- **Location**: `ui/app.js`, `ui/index.html`
- **Fix**: Add loading spinners, error message display

### 15. **Model Selection Limited**
- **Problem**: UI model dropdown has only one hardcoded option
- **Location**: `ui/index.html` line 22-24
- **Fix**: Make models configurable or fetch from API

### 16. **README Incomplete**
- **Problem**: Missing setup instructions, environment variables, usage examples
- **Location**: `README.md`
- **Fix**: Add comprehensive documentation

---

## 🟢 LOW PRIORITY / ENHANCEMENTS

### 17. **Missing .env.example File**
- **Problem**: No template for environment variables
- **Fix**: Create `.env.example` with all required variables

### 18. **Roo Adapter Issues**
- **Problem**: No error handling, hardcoded localhost URL
- **Location**: `adapters/roo_adapter.py`
- **Fix**: Add error handling, make URL configurable

### 19. **WebSocket Error Handling Incomplete**
- **Problem**: WebSocket handler has no error handling or cleanup
- **Location**: `app.py` lines 38-50
- **Fix**: Add try/except, proper connection cleanup

### 20. **API Documentation Missing**
- **Problem**: No custom OpenAPI/Swagger documentation
- **Location**: `app.py`
- **Fix**: Add detailed API descriptions and examples

---

## 📋 IMPLEMENTATION CHECKLIST

### Phase 1: Critical Fixes (Do First)
- [ ] Fix slowapi middleware integration
- [ ] Add CORS middleware
- [ ] Add error handling to all endpoints
- [ ] Add WebSocket authentication
- [ ] Add configuration validation

### Phase 2: High Priority
- [ ] Persist UI configuration
- [ ] Add WebSocket support to UI
- [ ] Fix VSCode extension dependencies
- [ ] Add VSCode extension configuration
- [ ] Add response validation
- [ ] Add health check endpoint

### Phase 3: Medium Priority
- [ ] Improve input validation
- [ ] Add logging
- [ ] Improve UI feedback
- [ ] Make models configurable
- [ ] Update README

### Phase 4: Polish
- [ ] Add .env.example
- [ ] Improve Roo adapter
- [ ] Improve WebSocket error handling
- [ ] Add API documentation

---

## 🔧 TECHNICAL DEBT

1. **Inconsistent Port Numbers**: UI defaults to `7860` but should match actual server port
2. **No Version Pinning**: `requirements.txt` has no version constraints
3. **Code Style**: Inconsistent formatting (some files use spaces, others don't)
4. **No Type Hints**: Python code lacks type hints
5. **Security**: Secret key defaults to "dev-secret" which is insecure

---

## 📊 RISK ASSESSMENT

| Issue | Severity | Likelihood | Impact |
|-------|----------|------------|--------|
| Missing CORS | High | High | UI completely broken |
| No Error Handling | High | High | Service crashes on errors |
| Rate Limiter Broken | Medium | Medium | API abuse possible |
| WebSocket No Auth | Medium | Low | Security vulnerability |
| Missing Config Validation | Medium | High | Silent failures |

---

## 🎯 SUCCESS CRITERIA

Project is production-ready when:
- ✅ All critical issues are fixed
- ✅ UI can successfully connect and make requests
- ✅ Error handling prevents crashes
- ✅ Configuration is validated on startup
- ✅ All dependencies are properly declared
- ✅ Basic documentation exists
- ✅ Health check endpoint works

---

## 📝 NOTES

- The project structure is good and well-organized
- The core functionality (API proxying) is sound
- Most issues are around error handling and configuration
- The UI and VSCode extension are functional but need polish

**Recommended order of work**: Fix critical issues first (1-5), then high priority (6-11), then work through medium/low priority as time permits.