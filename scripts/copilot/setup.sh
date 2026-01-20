#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd)"

log() { echo "==> $*"; }

# -------------------------
# Web setup (Node)
# -------------------------
setup_web() {
  # Detect a likely web root.
  # Preference order: ./web, ./frontend, ./client, else repo root if package.json exists.
  local candidates=("web" "frontend" "client" ".")
  local webdir=""

  for c in "${candidates[@]}"; do
    if [[ -f "$ROOT/$c/package.json" ]]; then
      webdir="$ROOT/$c"
      break
    fi
  done

  if [[ -z "$webdir" ]]; then
    log "Web: no package.json found in common locations; skipping."
    return 0
  fi

  log "Web: detected package.json at $(realpath --relative-to="$ROOT" "$webdir")"

  pushd "$webdir" >/dev/null

  # Enable corepack (pnpm/yarn) if present
  if command -v corepack >/dev/null 2>&1; then
    corepack enable || true
  fi

  # Auth for private registries if provided (safe: does not print tokens)
  if [[ -n "${NPM_TOKEN:-}" ]]; then
    log "Web: configuring NPM_TOKEN for private registry access"
    # Minimal npm auth line for GitHub Packages / private registries. Adjust registry if needed.
    npm config set "//registry.npmjs.org/:_authToken" "$NPM_TOKEN" >/dev/null 2>&1 || true
  fi

  if [[ -f "pnpm-lock.yaml" ]]; then
    log "Web: installing via pnpm"
    # Prefer packageManager field if present; else latest pnpm available via corepack.
    pnpm --version >/dev/null 2>&1 || corepack prepare pnpm@latest --activate
    pnpm install --frozen-lockfile

  elif [[ -f "yarn.lock" ]]; then
    log "Web: installing via yarn"
    yarn --version >/dev/null 2>&1 || true
    # yarn classic vs berry differences are handled by yarn itself; keep it deterministic.
    yarn install --immutable || yarn install --frozen-lockfile

  elif [[ -f "package-lock.json" ]]; then
    log "Web: installing via npm ci"
    npm ci

  else
    log "Web: no lockfile found; running npm install (best-effort, may be non-deterministic)"
    npm install
  fi

  # Optional: basic sanity check, but don't fail the whole setup if scripts are missing
  if jq -e '.scripts.build? != null' package.json >/dev/null 2>&1; then
    log "Web: prebuilding deps (best-effort)"
    npm run -s build || true
  fi

  popd >/dev/null
}

# -------------------------
# Android setup (Gradle)
# -------------------------
setup_android() {
  if [[ ! -f "$ROOT/gradlew" ]]; then
    log "Android: no ./gradlew found; skipping."
    return 0
  fi

  log "Android: preparing Gradle wrapper"
  chmod +x "$ROOT/gradlew"

  # Download wrapper + prime caches. Keep this safe and fairly fast.
  "$ROOT/gradlew" --no-daemon -q --version || true
  "$ROOT/gradlew" --no-daemon -q help || true

  # Best-effort prefetch build (does not fail the entire Copilot session).
  # We skip lint/test here because this is about dependency hydration, not correctness.
  log "Android: best-effort assemble to prefetch dependencies"
  "$ROOT/gradlew" --no-daemon --stacktrace assembleDebug -x lint -x test || true
}

# -------------------------
# Entrypoint
# -------------------------
log "Copilot environment bootstrap starting"
setup_web
setup_android
log "Copilot environment bootstrap complete"
