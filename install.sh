#!/usr/bin/env bash
# Install yt2skill into ~/.claude/skills/yt2skill/
set -euo pipefail
raw="https://raw.githubusercontent.com/qazaqninja/yt2skill/main"
dest="$HOME/.claude/skills/yt2skill"
mkdir -p "$dest"
for f in SKILL.md fetch_transcript.py; do
  curl -fsSL "$raw/$f" -o "$dest/$f"
done
chmod +x "$dest/fetch_transcript.py"
# Anonymous install counter (no PII beyond the request). Opt out: YT2SKILL_NO_TRACK=1
[ "${YT2SKILL_NO_TRACK:-}" ] || curl -fsS -m 5 "https://abacus.jasoncameron.dev/hit/qazaqninja-yt2skill/install" >/dev/null 2>&1 || true
echo "Installed yt2skill -> $dest"
echo "Run /yt2skill <youtube-url> in Claude Code (restart it first to pick up the skill)."
