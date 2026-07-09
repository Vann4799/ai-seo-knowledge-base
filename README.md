# AI-Powered SEO Content Production Research

Research project for collecting high-signal expert content about AI-powered SEO content production for B2B SaaS.

## Project Overview

This repository collects expert sources, LinkedIn research notes, and YouTube transcript targets for a future playbook on AI-powered SEO content production.

The goal is not to collect the most material possible. The goal is to collect strong practitioner material from people who are actively building, advising, testing, or teaching modern SEO, AEO/GEO, AI search visibility, and content production workflows.

## Why This Topic

AI-powered SEO content production is a strong research topic because it connects directly to current changes in search behavior, AI Overviews, answer engines, content quality, and scalable content operations.

It is also practical for this assignment because:

- There are many credible operators publishing current material.
- YouTube transcripts are available for several experts.
- LinkedIn posts can be collected manually where automation is unreliable.
- The topic naturally supports API usage and workflow automation.
- The output can support a real playbook later.

## Selected Experts

The selected experts are:

1. Kevin Indig
2. Ross Simmonds
3. Eli Schwartz
4. Bernard Huang
5. Gael Breton
6. Matt Diggity
7. Nathan Gotch
8. Lily Ray
9. Aleyda Solis
10. Cyrus Shepard

These experts were chosen because they are practitioners, founders, consultants, or senior SEO/content operators with public material on AI search, AEO/GEO, content optimization, content distribution, and SEO systems.

See [`research/sources.md`](research/sources.md) for links, annotations, and collection targets.

## Repository Structure

```text
research/
  sources.md
  expert-shortlist.md
  youtube-video-targets.csv
  linkedin-posts/
    <expert>/
      index.md
  youtube-transcripts/
  other/
scripts/
  download_youtube_transcripts.py
```

## Research Process

1. Selected the topic: AI-powered SEO content production.
2. Built a shortlist of expert candidates.
3. Verified 10 experts with public links and relevant recent content.
4. Added source annotations and transcript targets.
5. Created a YouTube transcript downloader script using the Supadata API.
6. Organized LinkedIn research notes by expert.

## Tools Used

- Codex for repo setup, research organization, and script generation.
- Web research for source verification.
- Supadata API target workflow for YouTube transcript collection.
- Manual LinkedIn collection for posts where scraping is not necessary or reliable.
- Git with small, staged commits to show progress over time.

## YouTube Transcript Collection

The transcript script is ready, but transcripts are not committed until the API is run.

Dry run:

```bash
python scripts/download_youtube_transcripts.py --manifest research/youtube-video-targets.csv --dry-run
```

Actual run:

```powershell
$env:SUPADATA_API_KEY="your_api_key"
python scripts/download_youtube_transcripts.py --manifest research/youtube-video-targets.csv
```

The script saves Markdown files under:

```text
research/youtube-transcripts/<expert>/
```

## Security Notes

- No API keys or credentials are stored in this repository.
- API keys should be provided through environment variables.
- LinkedIn collection is organized as linked notes and summaries, not credential-based scraping.
