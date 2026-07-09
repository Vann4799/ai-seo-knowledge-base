#!/usr/bin/env python3
"""Download YouTube transcripts with youtube-transcript-api."""

from __future__ import annotations

import argparse
import csv
import re
import sys
import time
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from youtube_transcript_api import YouTubeTranscriptApi


DEFAULT_OUTPUT_DIR = Path("research/youtube-transcripts")


@dataclass(frozen=True)
class VideoTarget:
    expert: str
    video_url: str
    notes: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download public YouTube captions and save Markdown transcript files."
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        required=True,
        help="CSV file with columns: expert,video_url,notes.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory. Default: {DEFAULT_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--languages",
        nargs="+",
        default=["en"],
        help="Caption language fallback order. Default: en.",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.5,
        help="Delay between videos. Default: 0.5 seconds.",
    )
    return parser.parse_args()


def load_manifest(path: Path) -> list[VideoTarget]:
    if not path.exists():
        raise SystemExit(f"Manifest not found: {path}")

    targets: list[VideoTarget] = []
    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        required = {"expert", "video_url"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"Manifest missing columns: {', '.join(sorted(missing))}")

        for row_number, row in enumerate(reader, start=2):
            expert = (row.get("expert") or "").strip()
            video_url = (row.get("video_url") or "").strip()
            notes = (row.get("notes") or "").strip()
            if not expert or not video_url:
                print(f"Skipping row {row_number}: expert or video_url is blank", file=sys.stderr)
                continue
            targets.append(VideoTarget(expert=expert, video_url=video_url, notes=notes))

    return targets


def extract_video_id(video_url: str) -> str:
    parsed = urllib.parse.urlparse(video_url)

    if parsed.netloc in {"youtu.be", "www.youtu.be"}:
        video_id = parsed.path.strip("/").split("/")[0]
        if video_id:
            return video_id

    query = urllib.parse.parse_qs(parsed.query)
    if "v" in query and query["v"]:
        return query["v"][0]

    path_parts = [part for part in parsed.path.split("/") if part]
    for marker in ("shorts", "embed", "live"):
        if marker in path_parts:
            index = path_parts.index(marker)
            if index + 1 < len(path_parts):
                return path_parts[index + 1]

    raise ValueError(f"Could not extract YouTube video ID from URL: {video_url}")


def slugify(value: str, fallback: str = "untitled") -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or fallback


def format_timestamp(seconds: Any) -> str:
    try:
        total_seconds = int(float(seconds))
    except (TypeError, ValueError):
        return ""

    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def fetch_transcript(video_id: str, languages: list[str]) -> list[dict[str, Any]]:
    fetched = YouTubeTranscriptApi().fetch(video_id, languages=languages)
    return [item.to_raw_data() for item in fetched]


def markdown_for(target: VideoTarget, video_id: str, transcript: list[dict[str, Any]]) -> str:
    lines = [
        "---",
        f'expert: "{escape_yaml(target.expert)}"',
        f'video_id: "{video_id}"',
        f'video_url: "{target.video_url}"',
        'source_method: "youtube-transcript-api"',
        "---",
        "",
        f"# YouTube Transcript - {target.expert}",
        "",
        f"- Expert: {target.expert}",
        f"- Source: {target.video_url}",
    ]

    if target.notes:
        lines.append(f"- Notes: {target.notes}")

    lines.extend(["", "## Transcript", ""])
    for segment in transcript:
        text = str(segment.get("text") or "").strip()
        if not text:
            continue

        timestamp = format_timestamp(segment.get("start"))
        if timestamp:
            lines.append(f"- [{timestamp}] {text}")
        else:
            lines.append(text)

    return "\n".join(lines).strip() + "\n"


def escape_yaml(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def output_path(output_dir: Path, expert: str, video_id: str) -> Path:
    expert_dir = output_dir / slugify(expert, "unknown-expert")
    filename = f"youtube-transcript-{video_id}.md"
    return expert_dir / filename


def main() -> int:
    args = parse_args()
    targets = load_manifest(args.manifest)
    if not targets:
        print("No targets found.", file=sys.stderr)
        return 1

    failures = 0
    for index, target in enumerate(targets, start=1):
        try:
            video_id = extract_video_id(target.video_url)
            transcript = fetch_transcript(video_id, args.languages)
            path = output_path(args.output_dir, target.expert, video_id)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(markdown_for(target, video_id, transcript), encoding="utf-8")
            print(f"Saved {path}")
        except Exception as error:  # noqa: BLE001 - keep processing remaining videos.
            failures += 1
            print(f"Failed {target.video_url}: {error}", file=sys.stderr)

        if index < len(targets) and args.sleep > 0:
            time.sleep(args.sleep)

    if failures:
        print(f"Completed with {failures} failure(s).", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

