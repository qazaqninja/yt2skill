# yt2skill

A Claude Code skill that turns a YouTube video into a reusable **agent skill**
(or subagent). It fetches the transcript, extracts the *transferable method*
taught in the video, and writes an installable `SKILL.md`.

## Use

```
/yt2skill <youtube-url> [--agent] [--name <slug>]
```

- `--agent` — emit a subagent (`~/.claude/agents/<slug>.md`) instead of a skill,
  for videos that describe a role/persona rather than a procedure.
- `--name` — force the generated skill's slug.

The new skill is written to `~/.claude/skills/<slug>/` and is live immediately.

## Files

- `SKILL.md` — the skill (the procedure Claude follows on `/yt2skill`).
- `fetch_transcript.py` — prints a video's transcript as plain text. Exit codes:
  `0` ok · `2` dep missing · `3` no captions · `4` bad url.

## Install

Symlinked into the skills dir (edits here apply live):

```bash
ln -sf "$PWD/SKILL.md" ~/.claude/skills/yt2skill/SKILL.md
ln -sf "$PWD/fetch_transcript.py" ~/.claude/skills/yt2skill/fetch_transcript.py
```

Transcript fetching needs `youtube-transcript-api` (the skill auto-installs it on
first run): `python3 -m pip install --user youtube-transcript-api`.

## Limits

No captions → no skill (it won't hallucinate one). A Whisper-from-audio fallback
is deliberately omitted as too heavy; add it only if you hit caption-less videos
often.

## Demo

Built from Julian Treasure's "How to speak so that people want to listen"
(`eIho2S0ZahI`) → the `speak-to-be-heard` skill.
