0) Non-Negotiable Rules (No Fake Work)
These rules prevent “docs-only” or “looks fine” nonsense.
No guessing. If something is unknown, the AI must locate the implementing file and confirm behavior by reading code + running tests.
No placeholders. Any feature claimed must be runnable and verified.
No partial wiring. If UI has a button, it must do something real or be removed.
No “it should work.” The AI must prove it with a repeatable verification step.
Preserve existing structure + styling. Fix layout bugs without redesigning.
Return a single complete ZIP containing all fixes, with no missing files and no broken imports.
1) Repository Inventory + Structure Integrity
Goal: ensure we’re inspecting the correct project and not a duplicate UI or stale file.
1.1 Confirm canonical root
Verify the project root contains (minimum):
app.py, config.py, rate_limit.py, requirements.txt
/ui/ folder (contains perplex_index2.html at minimum)
/agent/ folder (router/executor/planner logic)
Confirm no “shadow UI” is accidentally being edited (example: ui.zip contents vs ui/).
If multiple UIs exist (ui/perplex_index2.html and ui_zip/ui/index.html), pick the actual served one and document why.
1.2 File-by-file index
AI must generate an inventory and mark each file as:
USED (imported/executed/served),
UNUSED (dead code),
UNKNOWN (needs runtime confirmation)
Minimum scan:
app.py, start.py, config.py, rate_limit.py
/ui/perplex_index2.html (script + CSS + DOM)
/agent/* (router/executor/planner)
/adapters/*
/vscode_extension/* (if relevant)
2) Backend Inspection Checklist (FastAPI)
Goal: verify API endpoints, auth, streaming, terminal execution, error handling, and security constraints.
2.1 Static serving correctness
Confirm GET / serves the intended UI file:
If ui/index.html doesn’t exist but ui/perplex_index2.html does, root must still work.
Confirm app.mount("/ui", StaticFiles(...)) works and routes resolve:
/ui/perplex_index2.html loads without 404
assets load if required (/assets)
2.2 Authentication and headers
Verify auth middleware behavior:
Public paths skip auth (/health, /models, /docs, /openapi.json, /ui/*).
Protected paths require X-API-KEY == BRIDGE_SECRET.
Verify client UI sends correct headers (or explicitly doesn’t need them when hitting public endpoints).
2.3 /models endpoint compatibility
Confirm /models returns data in a structure the UI actually parses:
Preferred: { "models": [ { "id": "...", ... } ] }
Verify UI fallback behavior if API unreachable.
2.4 /v1/chat/completions proxy correctness
AI must verify:
Request shape passed to Perplexity is correct:
model, messages, temperature, max_tokens, frequency_penalty, stream as needed
Response validation is correct:
Must contain .choices[0].message.content for non-streaming.
Error handling:
502 for upstream errors, 504 for timeouts, 500 only for truly internal issues.
Rate limiting works (SlowAPI integration).
2.5 WebSocket endpoint (/ws/chat)
AI must validate:
Auth can be via query param api_key OR header X-API-KEY.
Streaming chunks are forwarded and do not break framing.
On disconnect, loop exits cleanly; no runaway tasks.
On upstream error, send structured error JSON then recover/close cleanly.
2.6 Terminal endpoint (POST /terminal) streaming verification
This is a high-risk feature. AI must validate it fully.
Required checks:
Endpoint exists and imports required things (StreamingResponse, asyncio etc).
It streams line output while process runs (not buffering everything).
It handles:
stderr output
non-zero exit codes
long-running commands
It has guardrails:
Working directory constraints or sandboxing (at minimum, avoid arbitrary rm -rf /)
Command length limit
Timeout kill
Explicit allowlist (recommended) or “safe mode” toggle
If guardrails are missing, AI must implement them. No exceptions.
Proof required:
Run echo hello, python --version, and one command that produces multiple lines (pip list or ls -la) and confirm streaming.
3) UI Inspection Checklist (ui/perplex_index2.html)
Goal: guarantee tab switching, layout, editor, file list, terminal, models, config forms, and streaming all work with no broken wiring.
3.1 DOM integrity (layout bugs)
AI must confirm:
Each tab exists exactly once:
chat-tab, history-tab, projects-tab, settings-tab, models-tab, stats-tab
projects-tab is not nested inside chat-tab.
No duplicated IDs.
No unclosed containers causing CSS bleed.
On small screens, layout doesn’t break:
file list scrolls, editor visible, terminal visible
no overflow pushing content off-screen
Proof required:
Open UI in browser at common widths:
mobile-ish (390px), tablet-ish (768px), desktop-ish (1280px)
3.2 Tab switching logic
Confirm switchTab(tabId):
Adds .active only to selected tab/button
Doesn’t leave tabs invisible
Confirm nav buttons data-tab="projects" etc match actual tab IDs.
3.3 “Dead wiring” purge or fix
For each button ID in UI, AI must confirm it has a working listener:
sendBtn, clearBtn, newChatBtn, favBtn, copyBtn, exportBtn
saveTempBtn (must do something real or removed)
voiceBtn (must do something real or removed)
Projects tab:
loadManifestBtn, saveEditorBtn, downloadEditorBtn, formatBtn
downloadFileBtn (selected file download)
Terminal: runTerminalBtn, Enter-to-run
3.4 Monaco Editor integration (no fake embedding)
AI must confirm:
Monaco loader script loads in served environment (not just file://)
Editor instantiates once and survives tab switching
Editor:
shows content from selected file
supports formatting (JSON, basic)
supports saving to local storage (or real saving if implemented)
supports download of current file
If Monaco cannot load (offline), UI must gracefully degrade to a fallback textarea (optional but recommended).
3.5 Project file list + selection behavior
File list renders from manifest JSON
Clicking a file:
highlights row (.selected)
loads file content into editor
updates filename indicator
Confirm paths resolve correctly relative to /ui/ (no broken ../ assumptions).
Confirm large file lists don’t freeze UI (limit or virtualize if needed).
3.6 Terminal UI streaming wiring
AI must verify:
UI sends terminal requests to backend /terminal
Output streams live into terminal window
UI handles:
interleaved stdout/stderr
partial chunks
command prompt echo
prevents HTML injection (escape output)
UI handles errors cleanly and doesn’t break future commands.
3.7 Model / rules / tool config exposure
AI must confirm:
cfg fields are fully editable from UI:
key, url, model selector, system prompt, temp, max tokens, frequency penalty
tools config JSON (shown and used)
rules config if present
Changes persist if intended (localStorage or in-memory).
3.8 Streaming chat mode behavior
AI must confirm:
Streaming mode uses supported mechanism:
fetch streaming parsing SSE chunks or WS (whichever project supports)
It updates the UI incrementally (not only final content).
It stops cleanly on [DONE].
It doesn’t duplicate the final message.
3.9 “No broken imports / console errors” rule
AI must run the UI and confirm:
No uncaught exceptions in console.
No missing script URLs.
No undefined functions called from listeners.
4) Agent + Multi-Agent / Tool-Calling Mode (Project-Specific)
Goal: not just “we have tools JSON,” but actual tool-calling mode and multi-agent orchestration where this project supports it.
4.1 Identify current agent architecture
AI must locate and read:
/agent/router.py
/agent/executor.py
/agent/planner.py (if present)
/adapters/roo_adapter.py (bridge adapter)
Then classify:
Single agent vs router-based multi-agent
Whether tools are only passed through vs actually executed locally
4.2 Tool-calling contract
AI must confirm what the upstream model supports:
If Perplexity endpoint supports OpenAI-like tools, verify payload compatibility.
If not supported, AI must:
implement local tool execution loop (safe subset), or
explicitly disable tool-calling mode and remove UI claims
4.3 Multi-agent mode “real”
If multi-agent mode is claimed:
Must have:
a coordinator (router/planner)
at least two agent roles with clear responsibilities
tool execution handler
a trace/log shown in UI (recommended)
Proof required:
A demo prompt that triggers:
planner decision,
tool execution,
final synthesis response.
If not possible with this backend/model, AI must not pretend. Implement what’s feasible and downgrade claims.
5) Security + Safety Checks (Especially Terminal)
Humans will absolutely type rm -rf and then blame the code.
Minimum required:
Terminal endpoint must be constrained:
allowlist commands OR restrict to project directory
block dangerous tokens (rm -rf /, :(){ :|:& };:, etc.)
timeout + kill
max output size / stream truncation
UI must escape terminal output and chat output to prevent HTML injection.
No secrets printed in UI logs:
API keys must not be dumped in console
localStorage keys must be reviewed for leakage
6) Automated Verification Script Checklist
AI must add or run a repeatable validation routine. Minimum:
Backend sanity
python -m py_compile app.py
Start server and check:
GET /health
GET /models
POST /v1/chat/completions (with dummy key or stub mode)
/ws/chat handshake
/terminal streaming test
UI sanity
Serve via FastAPI static route and open /ui/perplex_index2.html
Verify:
tabs show
projects file list renders
Monaco loads
terminal runs echo hello and streams output
If something fails, AI must:
identify exact file/line,
fix it,
rerun the same verification.
7) Fix Protocol (How AI Must Repair Issues)
When a failure is found, AI must follow this exact loop:
Reproduce: run the failing action and capture error output.
Locate: find the exact file + function + line responsible.
Diagnose: explain root cause in plain terms.
Fix: implement real code change.
Regression check: rerun the failing test + one related test.
Document: add a short entry to INSPECTION_REPORT.md:
what was broken
what changed
how to verify
8) Release Checklist (ZIP Quality Gate)
Before returning the final ZIP, AI must confirm:
No missing files
No broken imports
requirements.txt consistent with imports
UI file paths correct (/ui/...)
Terminal endpoint exists and works
Monaco loads or gracefully degrades
Tools config is actually used in payloads
No duplicate tab IDs, no layout nesting bugs
The ZIP contains only the intended project (no extra junk directories)
9) “If You Claim It Works, Prove It” Evidence List
The AI must provide, in the final report, these proofs:
Output from:
python -m py_compile app.py
/health response
/models response
one terminal command streamed
A short “manual test script” of click steps that reproduces:
file selection -> editor content
terminal command -> streaming output
tools config saved -> used in payload