# AI-Powered SEO Content Production Research

Research project for collecting high-signal expert content about AI-powered SEO content production for B2B SaaS.

## Project Overview

This repository collects expert sources, LinkedIn post records, and YouTube transcripts for a future playbook on AI-powered SEO content production.

The goal is not to collect the most material possible. The goal is to collect strong practitioner material from people who are actively building, advising, testing, or teaching modern SEO, AEO/GEO, AI search visibility, and content production workflows.

## Objectives

- Identify 10 high-signal experts on AI-powered SEO content production.
- Collect links, annotations, and recent content targets for each expert.
- Organize LinkedIn research notes by author.
- Prepare and run a repeatable YouTube transcript workflow using an API-based script.
- Produce an initial synthesis that can support a practical playbook later.

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

## Expert Selection Criteria

Experts were selected using these criteria:

- Direct experience in SEO, AI search, organic growth, content strategy, or content operations.
- Evidence of recent public thinking on AI SEO, AEO/GEO, or AI-assisted content workflows.
- Public sources available through LinkedIn, websites, newsletters, podcasts, YouTube, or webinars.
- Practical operator perspective rather than generic commentary.
- Coverage diversity across B2B SaaS, technical SEO, content optimization, AI visibility, and distribution.

## Repository Structure

```text
research/
  sources.md
  expert-shortlist.md
  summary.md
  transcript-collection-log.md
  youtube-video-targets.csv
  linkedin-posts/
    <expert>/
      index.md
  youtube-transcripts/
    <expert>/
      <video-title>-<video-id>.md
  other/
scripts/
  download_youtube_transcripts.py
  download_youtube_transcripts_free.py
```

## Research Methodology

1. Selected the topic: AI-powered SEO content production.
2. Built a shortlist of expert candidates.
3. Verified 10 experts with public links and relevant recent content.
4. Added source annotations and transcript targets.
5. Created and ran a YouTube transcript downloader script using the Supadata API.
6. Collected 10 YouTube transcript Markdown files.
7. Organized LinkedIn research notes by expert.
8. Added an initial synthesis of recurring insights and strategy patterns.

## Data Collection Process

The research uses three collection lanes:

- Source mapping: expert profiles, websites, newsletters, and video channels are documented in [`research/sources.md`](research/sources.md).
- LinkedIn research: 20 selected public LinkedIn post records are organized by expert under [`research/linkedin-posts/`](research/linkedin-posts/) and consolidated in [`research/linkedin-posts/manifest.csv`](research/linkedin-posts/manifest.csv).
- YouTube transcripts: transcript targets are listed in [`research/youtube-video-targets.csv`](research/youtube-video-targets.csv), collected with [`scripts/download_youtube_transcripts.py`](scripts/download_youtube_transcripts.py), and saved under [`research/youtube-transcripts/`](research/youtube-transcripts/).

## Tools Used

- Codex for repo setup, research organization, and script generation.
- Web research for source verification.
- Supadata API target workflow for YouTube transcript collection.
- `youtube-transcript-api` and `yt-dlp` were tested as free transcript collection methods.
- Manual LinkedIn collection for posts where scraping is not necessary or reliable.
- Git with small, staged commits to show progress over time.

## Automation

The automation layer is intentionally narrow and safe:

- It reads targets from a CSV manifest.
- It uses `SUPADATA_API_KEY` from the environment.
- It writes one Markdown transcript per expert/video.
- It supports `--dry-run` so targets can be validated before making API calls.
- It handles per-video errors without storing credentials in the repository.

The repository also includes a free-method script using `youtube-transcript-api`:

```bash
python scripts/download_youtube_transcripts_free.py --manifest research/youtube-video-targets.csv
```

## YouTube Transcript Collection

10 YouTube transcript files have been collected via Supadata and committed under [`research/youtube-transcripts/`](research/youtube-transcripts/).

Collection attempts, blockers, and final successful API run are documented in [`research/transcript-collection-log.md`](research/transcript-collection-log.md).

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

## Limitations

- Free transcript methods were attempted, but YouTube blocked requests from the current environment.
- LinkedIn research is manually collected from public pages and search results as linked post records, so it may not represent every recent post by each expert.
- Some experts have stronger newsletter or webinar material than YouTube material.
- This repository is a research base, not the final AI SEO playbook.

## Lessons Learned

- Expert quality matters more than source volume.
- AI SEO research is strongest when it combines strategy, content systems, technical SEO, and distribution.
- Fully automated collection is not always the best choice; manual LinkedIn notes are acceptable when they create cleaner, more reliable context.
- A clear repo structure makes the research easier to audit and extend.

## Initial Synthesis

See [`research/summary.md`](research/summary.md) for early insights, recurring patterns, and gaps to address after transcript collection.
