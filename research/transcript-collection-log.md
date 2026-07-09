# Transcript Collection Log

Date checked: 2026-07-09.

This log documents transcript collection attempts for the YouTube targets in `research/youtube-video-targets.csv`.

## Target Manifest

- File: `research/youtube-video-targets.csv`
- Targets: 10 videos, one per selected expert
- Output folder: `research/youtube-transcripts/`

## Method 1: Supadata API

Script:

```powershell
$env:SUPADATA_API_KEY="your_api_key"
python scripts/download_youtube_transcripts.py --manifest research/youtube-video-targets.csv
```

Status:
Not run because no API key is stored in the repository.

Reason:
The project intentionally avoids committing API keys or credentials. The script is ready for use once `SUPADATA_API_KEY` is provided through the environment.

## Method 2: youtube-transcript-api

Script:

```powershell
python scripts/download_youtube_transcripts_free.py --manifest research/youtube-video-targets.csv
```

Status:
Attempted from the local environment.

Result:
All 10 targets failed because YouTube blocked transcript requests from the current IP/environment.

Observed error category:

```text
Could not retrieve a transcript...
YouTube is blocking requests from your IP.
```

## Method 3: yt-dlp subtitles

Test command:

```powershell
python -m yt_dlp --skip-download --write-auto-subs --write-subs --sub-lang en --sub-format vtt -o ".tmp-transcripts/%(id)s.%(ext)s" "https://www.youtube.com/watch?v=x5CgYCRLgbc"
```

Status:
Attempted with one target video.

Result:
Subtitle download failed due to YouTube rate limiting.

Observed error category:

```text
HTTP Error 429: Too Many Requests
```

## Method 4: Google timedtext endpoint

Test command:

```powershell
Invoke-WebRequest -Uri "https://video.google.com/timedtext?lang=en&v=x5CgYCRLgbc" -UseBasicParsing -TimeoutSec 30
```

Status:
Attempted with one target video.

Result:
Request was blocked by Google automated-query protection from the current network.

Observed error category:

```text
We're sorry... your computer or network may be sending automated queries.
```

## Next Best Step

Use the Supadata API script from a normal authenticated API workflow:

```powershell
$env:SUPADATA_API_KEY="your_api_key"
python scripts/download_youtube_transcripts.py --manifest research/youtube-video-targets.csv
```

If Supadata is unavailable, rerun the free script from a non-blocked residential connection:

```powershell
python scripts/download_youtube_transcripts_free.py --manifest research/youtube-video-targets.csv
```

## Notes

- No fake transcripts were created.
- No API keys or credentials were committed.
- The transcript folder includes documentation and is ready for generated Markdown outputs.
