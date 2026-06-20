---
name: yt2skill
description: "Turn a YouTube video into a reusable agent skill (or subagent). Fetches the transcript, extracts the teachable procedure, and writes an installable SKILL.md. Use when the user gives a YouTube URL and wants its method codified — 'make a skill from this video', 'yt2skill <url>'."
argument-hint: "<youtube-url> [--agent] [--name <slug>]"
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
---

<objective>
Input: a YouTube URL. Output: a new, installed agent skill (or subagent) that
captures the *transferable method* taught in the video — not a summary of the
video. The video is the source; the skill is a procedure the agent can re-run.
</objective>

## Flow

**1. Get the transcript.** From this skill's own directory:

```bash
D="$(dirname "$(readlink -f ~/.claude/skills/yt2skill/SKILL.md)")"
python3 "$D/fetch_transcript.py" "<URL>" > /tmp/yt2skill.txt; echo "exit=$?"
```

Handle the exit code:
- `0` — read `/tmp/yt2skill.txt`.
- `2` (NEED_INSTALL) — `python3 -m pip install --user --quiet youtube-transcript-api`, then rerun.
- `3` (no captions) — tell the user this video has no transcript; offer to let them paste one, or stop. Do not invent content.
- `4` (bad url) — ask for a valid URL.

**2. Read the transcript and extract the method.** Identify what the video
*teaches you to do*: the steps, rules, heuristics, gotchas, and order of
operations. Strip filler, sponsorships, and intros. If the video is pure
commentary with no transferable procedure, say so and stop — not everything is a
skill.

**3. Decide skill vs subagent** (default: skill):
- **Skill** — a procedure/checklist the agent runs on request. The common case.
- **Subagent** (`--agent`, or when the video describes a *role/persona* doing
  open-ended judgement work) — write a `~/.claude/agents/<slug>.md` instead, with
  `name`/`description`/`tools` frontmatter and a system prompt in the persona.

**4. Write it.** Pick a short kebab-case `<slug>` (or use `--name`). For a skill:

`~/.claude/skills/<slug>/SKILL.md`:
```markdown
---
name: <slug>
description: "<one line: what it does + when to use it, third person>"
---

# <Title>

<2-3 lines: what method this is and where it came from (video URL).>

## Steps
1. ...
2. ...

## Rules / gotchas
- ...
```

Rules for a good generated skill:
- Imperative steps the agent can *act* on, not prose about the video.
- Concrete: thresholds, commands, orderings — whatever the video specified.
- Keep the video URL in a one-line `Source:` footer for provenance.
- Ponytail: only the steps that matter. No invented sections, no boilerplate.

**5. Confirm + report.** Show the path and the one-line description. The skill is
live immediately (`~/.claude/skills/` is auto-discovered); a subagent likewise.
Tell the user the trigger (`/<slug>` or the agent name).

## Notes
- No captions → no skill. Whisper-from-audio fallback is intentionally not built
  (heavy: yt-dlp + ffmpeg + model). Add it only if a user hits this repeatedly.
- Don't overfit to one example in the video — capture the general method.
