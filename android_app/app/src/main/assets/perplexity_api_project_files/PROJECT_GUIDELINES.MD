# PROJECT GUIDELINES — PERPLEXITY BRIDGE PRO

## 1. PROJECT INTENT
Perplexity Bridge Pro exists to:
- act as a **stable, deterministic bridge**
- normalize access to Perplexity-style APIs
- support multiple adapters cleanly
- survive API changes without cascading failures

This is infrastructure software.

---

## 2. DEVELOPMENT PHILOSOPHY

### 2.1 Predictability Over Features
A boring system that works is superior to a clever system that breaks.

### 2.2 Explicit Over Implicit
If something happens:
- it must be visible in code
- it must be documented
- it must be configurable

---

## 3. CODING STANDARDS

### Python Style
- Python 3.x only
- No dynamic monkey-patching
- No runtime mutation of module globals
- Type hints strongly encouraged

### Error Handling
- Fail loudly at boundaries
- Fail early on misconfiguration
- Never auto-recover silently

---

## 4. ADAPTER DESIGN GUIDELINES

Each adapter MUST:
- represent exactly one external system
- expose a minimal surface area
- validate inputs aggressively
- return normalized responses

Adapters MUST NOT:
- manage config loading
- manage rate limiting
- log secrets

---

## 5. CONFIGURATION GUIDELINES
- `env.example` is authoritative
- Every config option must be documented
- No “optional but required” settings

If a value is required, enforce it.

---

## 6. LOGGING GUIDELINES
- INFO: lifecycle events
- WARNING: recoverable anomalies
- ERROR: actionable failures only

No log spam.
No emotional logs.
No jokes.

---

## 7. USER EXPERIENCE RULES
- Clear startup errors
- Deterministic shutdown
- No hanging processes
- No unexplained delays

If the user is confused, the system failed.

---

## 8. MAINTENANCE EXPECTATIONS
- Backward compatibility is the default
- Breaking changes require documentation updates
- ROADMAP.md must be updated with intent, not hype

---

## 9. CONTRIBUTION SAFETY CHECK
Before merging:
- Can this be removed cleanly?
- Does this make debugging harder?
- Does this increase mental load?

If yes → rethink.

---

## 10. GUIDELINE SUMMARY
Stable.
Explicit.
Composable.
Predictable.

Anything else is noise.