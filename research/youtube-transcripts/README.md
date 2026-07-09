# YouTube Transcripts

This folder is reserved for transcript files generated from `research/youtube-video-targets.csv`.

Transcripts are not committed yet because the project does not store API keys, and free transcript requests were blocked from the current environment.

Supadata workflow:

```powershell
$env:SUPADATA_API_KEY="your_api_key"
python scripts/download_youtube_transcripts.py --manifest research/youtube-video-targets.csv
```

Free-method workflow:

```powershell
python scripts/download_youtube_transcripts_free.py --manifest research/youtube-video-targets.csv
```

Expected output format:

```text
research/youtube-transcripts/<expert>/<video-title>-<video-id>.md
```

Each generated Markdown file includes video metadata, source URL, expert name, and transcript text.

See `research/transcript-collection-log.md` for collection attempts and blockers.
