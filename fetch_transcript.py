#!/usr/bin/env python3
"""Print a YouTube video's transcript as plain text.

Usage: python3 fetch_transcript.py <url-or-id> [lang]
Exit codes: 0 ok | 2 missing dep | 3 no transcript | 4 bad url
"""
import re
import sys


def video_id(s: str) -> str | None:
    s = s.strip()
    if re.fullmatch(r"[\w-]{11}", s):
        return s
    m = re.search(r"(?:v=|/shorts/|/embed/|youtu\.be/)([\w-]{11})", s)
    return m.group(1) if m else None


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: fetch_transcript.py <url-or-id> [lang]", file=sys.stderr)
        return 4
    vid = video_id(sys.argv[1])
    if not vid:
        print(f"could not extract a video id from: {sys.argv[1]}", file=sys.stderr)
        return 4
    langs = [sys.argv[2]] if len(sys.argv) > 2 else ["en", "en-US", "en-GB"]

    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        print("NEED_INSTALL youtube-transcript-api", file=sys.stderr)
        return 2

    # API shape changed across versions; try new instance API then legacy classmethod.
    try:
        try:
            chunks = YouTubeTranscriptApi().fetch(vid, languages=langs)
            segments = [getattr(c, "text", "") for c in chunks]
        except (AttributeError, TypeError):
            chunks = YouTubeTranscriptApi.get_transcript(vid, languages=langs)
            segments = [c["text"] for c in chunks]
    except Exception as e:  # NoTranscriptFound / TranscriptsDisabled / network
        # Last resort: any available language.
        try:
            chunks = YouTubeTranscriptApi.get_transcript(vid)
            segments = [c["text"] for c in chunks]
        except Exception:
            print(f"no transcript available for {vid}: {e}", file=sys.stderr)
            return 3

    text = " ".join(t.strip() for t in segments if t and t.strip())
    text = re.sub(r"\s+", " ", text).strip()
    print(f"# transcript: youtube.com/watch?v={vid}\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
