# YouTube Transcripts

This folder is reserved for transcript files generated from `research/youtube-video-targets.csv`.

Transcripts are not committed yet because the project does not store API keys. To collect them, run:

```powershell
$env:SUPADATA_API_KEY="your_api_key"
python scripts/download_youtube_transcripts.py --manifest research/youtube-video-targets.csv
```

Expected output format:

```text
research/youtube-transcripts/<expert>/<video-title>-<video-id>.md
```

Each generated Markdown file includes video metadata, source URL, expert name, and transcript text.

