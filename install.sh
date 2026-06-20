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
echo "Installed yt2skill -> $dest"
echo "Run /yt2skill <youtube-url> in Claude Code (restart it first to pick up the skill)."
