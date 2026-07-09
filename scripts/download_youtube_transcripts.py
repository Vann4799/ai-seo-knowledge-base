#!/usr/bin/env python3
"""Download YouTube transcripts with Supadata and save them as Markdown."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


BASE_URL = "https://api.supadata.ai/v1"
DEFAULT_OUTPUT_DIR = Path("research/youtube-transcripts")


@dataclass(frozen=True)
class VideoTarget:
    expert: str
    video_url: str
    notes: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download YouTube transcripts via Supadata and save Markdown files."
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        help="CSV file with columns: expert,video_url,notes.",
    )
    parser.add_argument("--expert", help="Expert name for a single video download.")
    parser.add_argument("--video-url", help="YouTube URL for a single video download.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory. Default: {DEFAULT_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--lang",
        default="en",
        help="Transcript language code. Default: en.",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.25,
        help="Delay between API calls when using a manifest. Default: 0.25 seconds.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate inputs and show planned files without calling the API.",
    )
    return parser.parse_args()


def load_targets(args: argparse.Namespace) -> list[VideoTarget]:
    if args.manifest:
        return load_manifest(args.manifest)

    if args.expert and args.video_url:
        return [VideoTarget(expert=args.expert, video_url=args.video_url)]

    raise SystemExit("Provide either --manifest or both --expert and --video-url.")


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


def supadata_get(path: str, params: dict[str, str], api_key: str) -> dict[str, Any]:
    query = urllib.parse.urlencode(params)
    request = urllib.request.Request(
        f"{BASE_URL}{path}?{query}",
        headers={"x-api-key": api_key, "accept": "application/json"},
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Supadata HTTP {error.code}: {error_body}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"Supadata request failed: {error.reason}") from error

    try:
        return json.loads(body)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Supadata returned invalid JSON: {body[:500]}") from error


def get_video_metadata(video_id: str, api_key: str) -> dict[str, Any]:
    return supadata_get("/youtube/video", {"id": video_id}, api_key)


def get_transcript(video_id: str, lang: str, api_key: str) -> list[dict[str, Any]]:
    data = supadata_get("/youtube/transcript", {"videoId": video_id, "lang": lang}, api_key)
    content = data.get("content")
    if not isinstance(content, list):
        raise RuntimeError(f"Transcript response did not include a content list for {video_id}")
    return [normalize_segment(segment) for segment in content]


def normalize_segment(segment: Any) -> dict[str, Any]:
    if isinstance(segment, str):
        return {"text": segment}
    if isinstance(segment, dict):
        return segment
    return {"text": str(segment)}


def slugify(value: str, fallback: str = "untitled") -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or fallback


def format_timestamp(seconds: Any) -> str:
    if seconds is None or seconds == "":
        return ""
    if isinstance(seconds, str):
        parts = seconds.split(":")
        if len(parts) == 2 and all(part.isdigit() for part in parts):
            return f"00:{int(parts[0]):02d}"
        if len(parts) == 3 and all(part.isdigit() for part in parts):
            return f"{int(parts[0]):02d}:{int(parts[1]):02d}"

    try:
        total_seconds = int(float(seconds))
    except (TypeError, ValueError):
        return str(seconds)

    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def markdown_for(
    target: VideoTarget,
    video_id: str,
    metadata: dict[str, Any],
    transcript: list[dict[str, Any]],
    lang: str,
) -> str:
    title = metadata.get("title") or f"YouTube video {video_id}"
    channel = metadata.get("channelTitle") or metadata.get("author") or ""
    published_at = metadata.get("publishedAt") or metadata.get("publishDate") or ""

    lines = [
        "---",
        f'title: "{escape_yaml(str(title))}"',
        f'expert: "{escape_yaml(target.expert)}"',
        f'video_id: "{video_id}"',
        f'video_url: "{target.video_url}"',
        f'channel: "{escape_yaml(str(channel))}"',
        f'published_at: "{escape_yaml(str(published_at))}"',
        f'language: "{lang}"',
        "---",
        "",
        f"# {title}",
        "",
        f"- Expert: {target.expert}",
        f"- Source: {target.video_url}",
    ]
    if channel:
        lines.append(f"- Channel: {channel}")
    if published_at:
        lines.append(f"- Published: {published_at}")
    if target.notes:
        lines.append(f"- Notes: {target.notes}")

    lines.extend(["", "## Transcript", ""])
    for segment in transcript:
        text = str(segment.get("text") or "").strip()
        if not text:
            continue

        timestamp = (
            segment.get("start")
            or segment.get("offset")
            or segment.get("timestamp")
            or segment.get("startTime")
        )
        formatted = format_timestamp(timestamp)
        if formatted:
            lines.append(f"- [{formatted}] {text}")
        else:
            lines.append(text)

    return "\n".join(lines).strip() + "\n"


def escape_yaml(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def output_path(output_dir: Path, expert: str, title: str, video_id: str) -> Path:
    expert_dir = output_dir / slugify(expert, "unknown-expert")
    filename = f"{slugify(title, video_id)}-{video_id}.md"
    return expert_dir / filename


def process_target(target: VideoTarget, args: argparse.Namespace, api_key: str | None) -> Path:
    video_id = extract_video_id(target.video_url)

    if args.dry_run:
        planned = output_path(args.output_dir, target.expert, f"youtube-video-{video_id}", video_id)
        print(f"DRY RUN: {target.expert} -> {planned}")
        return planned

    if not api_key:
        raise RuntimeError("SUPADATA_API_KEY is required unless --dry-run is used.")

    metadata = get_video_metadata(video_id, api_key)
    transcript = get_transcript(video_id, args.lang, api_key)
    title = str(metadata.get("title") or f"YouTube video {video_id}")
    path = output_path(args.output_dir, target.expert, title, video_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        markdown_for(target, video_id, metadata, transcript, args.lang),
        encoding="utf-8",
    )
    print(f"Saved {path}")
    return path


def main() -> int:
    args = parse_args()
    targets = load_targets(args)
    if not targets:
        print("No targets found.", file=sys.stderr)
        return 1

    api_key = os.environ.get("SUPADATA_API_KEY")
    failures = 0

    for index, target in enumerate(targets, start=1):
        try:
            process_target(target, args, api_key)
        except Exception as error:  # noqa: BLE001 - command-line tool should continue per target.
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
