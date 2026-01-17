# PROJECT RULES — PERPLEXITY BRIDGE PRO

## 0. NON-NEGOTIABLE PRINCIPLE
This project is a **production integration bridge**, not a demo, not a playground, and not a proof-of-concept.

Anything that degrades:
- reliability
- determinism
- compatibility
- rate-limit safety
- adapter isolation

is considered a **regression**.

---

## 1. SOURCE OF TRUTH
The authoritative sources are:
1. `app.py` — runtime orchestration
2. `config.py` — configuration contract
3. `adapters/` — interface boundary enforcement
4. `rate_limit.py` — safety and compliance layer
5. `ROADMAP.md` — planned evolution (must not be contradicted)

No change may violate assumptions made by these files.

---

## 2. IMMUTABLE ARCHITECTURE CONSTRAINTS

### 2.1 Adapter Boundary Rule
- All external system logic **MUST** live in `adapters/`
- `app.py` **MUST NEVER** contain provider-specific logic
- Adapters communicate via **explicit, typed, documented interfaces**
- No adapter may import another adapter directly

Violation = hard rejection.

---

### 2.2 Configuration Isolation
- `config.py` defines configuration structure, not secrets
- Secrets **MUST ONLY** come from:
  - environment variables
  - `.env` files (user-provided, never committed)
- No fallback defaults for secrets are allowed

Silent defaults are forbidden.

---

### 2.3 Rate-Limit Authority
`rate_limit.py` is the **single enforcement point**.

Rules:
- No adapter may implement its own rate limiting
- No retry logic may bypass `rate_limit.py`
- No exponential backoff duplication allowed

All request throttling flows through this module.

---

## 3. FILE-LEVEL RULES

### app.py
- Orchestration only
- No business logic
- No provider logic
- Must remain readable top-to-bottom without scrolling confusion

### adapters/*.py
- One provider or protocol per adapter
- Must expose:
  - explicit init
  - explicit request execution
  - explicit error surface
- No global state

### rate_limit.py
- Deterministic behavior required
- No background threads without explicit lifecycle control
- All timing must be monotonic

---

## 4. PLATFORM COMPATIBILITY RULES
The project **MUST remain functional** on:
- Windows (batch + VBS launchers)
- macOS
- Linux (desktop + CLI)

No OS-specific assumptions allowed in core logic.

---

## 5. FORBIDDEN PRACTICES
❌ Hardcoded API keys  
❌ Silent exception swallowing  
❌ Magic numbers without explanation  
❌ Hidden network calls  
❌ Background threads without shutdown control  
❌ Implicit adapter discovery  

---

## 6. CHANGE ACCEPTANCE CRITERIA
A change is acceptable ONLY if:
- It does not break existing adapters
- It does not require undocumented configuration
- It does not introduce hidden state
- It can be disabled cleanly

If any of these fail → reject.

---

## 7. SECURITY BASELINE
- No logging of raw credentials
- No logging of full request payloads by default
- Debug logging must be explicitly enabled

Security regressions override all feature priorities.

---

## 8. FINAL RULE
If a change makes the system **harder to reason about**, it is wrong.

Clarity beats cleverness.