# YouTube Transcripts

This folder contains transcript files generated from `research/youtube-video-targets.csv`.

10 transcript files were collected with the Supadata workflow. The project does not store API keys; the key was provided through the `SUPADATA_API_KEY` environment variable.

Supadata workflow:

```powershell
$env:SUPADATA_API_KEY="your_api_key"
python scripts/download_youtube_transcripts.py --manifest research/youtube-video-targets.csv
```

Free-method workflow:

```powershell
python scripts/download_youtube_transcripts_free.py --manifest research/youtube-video-targets.csv
```

Output format:

```text
research/youtube-transcripts/<expert>/<video-title>-<video-id>.md
```

Each generated Markdown file includes video metadata, source URL, expert name, and transcript text.

See `research/transcript-collection-log.md` for collection attempts, blockers, and the final successful API run.
