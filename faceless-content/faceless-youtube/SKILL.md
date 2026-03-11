---
name: faceless-youtube
description: End-to-end faceless YouTube channel automation — from niche research and scripting through voiceover, video assembly, SEO optimization, and upload. Use this skill whenever the user mentions faceless YouTube, YouTube automation, AI-generated video content, YouTube scripting, YouTube SEO, video pipeline, content mill, or wants to create YouTube videos without showing their face. Also trigger when the user asks about YouTube monetization strategy, bulk video production, or automating any part of the YouTube content creation workflow. Covers the full pipeline (research → script → voice → visuals → edit → optimize → upload) with CLI-first tooling.
---

# Faceless YouTube Channel Automation

## Overview

This skill orchestrates the complete pipeline for producing faceless YouTube videos at scale using CLI tools and Claude. The philosophy: Claude handles the creative/strategic work (research, scripting, SEO), CLI tools handle media generation, and the human handles quality control and channel strategy.

**Pipeline stages:**
1. Niche Research & Topic Selection
2. Script Writing
3. Voiceover Generation
4. Visual Asset Creation & Video Assembly
5. SEO Optimization (Title, Description, Tags, Thumbnail)
6. Upload & Scheduling

For detailed tool setup and configuration, read `references/tool-stack.md`.
For deep-dive scripting techniques, read `references/scripting-guide.md`.
For SEO strategy, read `references/seo-guide.md`.

---

## Stage 1: Niche Research & Topic Selection

**Tool: Claude (native — no external tools needed)**

When the user needs topic ideas or niche validation, follow this process:

### Niche Selection Criteria
Score potential niches on these factors (1-10 each):
- **Search volume**: Are people actively searching for this? (check via YouTube autocomplete, Google Trends)
- **Competition density**: How saturated is the niche with faceless channels already?
- **CPM potential**: Finance/tech/B2B niches pay $15-40 CPM. Entertainment/gaming pay $2-7 CPM.
- **Evergreenness**: Will videos get views in 12 months? Evergreen > trending.
- **Faceless compatibility**: Can you tell compelling stories without a face? (History, science, finance = yes. Vlogs, reactions = no.)
- **Scriptability**: Can Claude write authoritative scripts on this topic? (Factual domains > opinion domains)

### Topic Ideation Framework
For any niche, generate topics using these angles:
1. **"Top N" / Listicles** — "10 Most Dangerous Roads in the World" (high CTR, easy to script)
2. **Explainers** — "How [Complex Thing] Actually Works" (evergreen, high watch time)
3. **Comparisons** — "X vs Y: Which Is Actually Better?" (drives engagement)
4. **Stories/Narratives** — "The Man Who [Did Incredible Thing]" (highest retention)
5. **Contrarian/Myth-busting** — "Why Everything You Know About X Is Wrong" (CTR magnet)

### Competitive Analysis
If the user wants to research existing channels:
```bash
# Use yt-dlp to pull metadata from competitor channels
yt-dlp --flat-playlist --print "%(title)s | %(view_count)s | %(upload_date)s" "https://www.youtube.com/@ChannelName/videos" | head -50
```
This shows what's working (high views relative to subscriber count = good topic signal).

---

## Stage 2: Script Writing

**Tool: Claude (native)**

This is where 70-80% of video quality is determined. Read `references/scripting-guide.md` for the full framework, but here's the core structure:

### Script Structure (for 8-12 minute videos, the sweet spot for monetization)
```
HOOK (0:00-0:30)     — 2-3 sentences. Pattern interrupt. Make them NEED to know.
CONTEXT (0:30-1:30)  — Set up why this matters. Create stakes.
BODY (1:30-9:00)     — 3-5 main points. Each point: claim → evidence → implication.
CLIMAX (9:00-10:30)  — The payoff. Deliver on the hook's promise.
CTA (10:30-11:00)    — Subscribe, comment prompt, next video tease.
```

### Script Output Format
Always output scripts in this format so downstream tools can parse them:

```
---
TITLE: [Working title]
TARGET_LENGTH: [minutes]
TONE: [conversational/authoritative/dramatic/humorous]
PACING: [words per minute — 150 for dramatic, 170 for conversational, 190 for energetic]
---

[HOOK]
[Script text here. Write for the EAR, not the eye. Short sentences. Conversational.]

[VISUAL: Description of what should be on screen during this section]

[CONTEXT]
[Script text...]

[VISUAL: ...]

[BODY - POINT 1: Title of point]
[Script text...]

[VISUAL: ...]

... and so on
```

The `[VISUAL: ...]` tags are critical — they become prompts for video generation in Stage 4.

### Key Scripting Rules
- Write at a 7th-8th grade reading level. YouTube audiences skim.
- One idea per sentence. One theme per paragraph.
- Use "you" constantly. "Here's what happens when YOU..." not "One might observe..."
- Front-load value. YouTube counts the first 30 seconds. Don't waste them.
- Include 2-3 "open loops" — tease something coming later to prevent drop-off.
- Word count targets: ~1,500 words = 8 min, ~2,000 words = 11 min, ~2,500 words = 14 min (at 170 WPM).

---

## Stage 3: Voiceover Generation

**Primary tool: `edge-tts` (FREE, CLI, no API key needed)**
**Paid alternative: ElevenLabs API ($5-22/mo)**

### Option A: edge-tts (Free, CLI-native)
```bash
# Install
pip install edge-tts

# List available voices (there are 400+)
edge-tts --list-voices

# Recommended voices for faceless YouTube:
# Male:   en-US-GuyNeural (warm, natural), en-US-AndrewNeural (authoritative)
# Female: en-US-JennyNeural (conversational), en-US-AriaNeural (energetic)

# Generate voiceover
edge-tts --voice "en-US-GuyNeural" --file script.txt --write-media voiceover.mp3

# With rate/pitch adjustment
edge-tts --voice "en-US-GuyNeural" --rate="+10%" --pitch="+2Hz" --file script.txt --write-media voiceover.mp3

# Generate subtitle file simultaneously
edge-tts --voice "en-US-GuyNeural" --file script.txt --write-media voiceover.mp3 --write-subtitles voiceover.vtt
```

### Option B: ElevenLabs API ($5-22/mo, higher quality)
```bash
# Install
pip install elevenlabs

# Via CLI (after setting ELEVEN_API_KEY)
python3 -c "
from elevenlabs import generate, save, set_api_key
set_api_key('YOUR_KEY')
audio = generate(text=open('script.txt').read(), voice='Adam', model='eleven_monolingual_v1')
save(audio, 'voiceover.mp3')
"
```

### Option C: Kokoro TTS (Free, local, high quality, requires GPU or patience)
Newer open-source option. Quality approaching ElevenLabs. Runs locally.
```bash
pip install kokoro-onnx
# See references/tool-stack.md for full Kokoro setup
```

### Post-processing (always do this)
```bash
# Normalize audio levels
ffmpeg -i voiceover.mp3 -af "loudnorm=I=-16:TP=-1.5:LRA=11" voiceover_normalized.mp3

# Optional: add subtle background music
ffmpeg -i voiceover_normalized.mp3 -i background_music.mp3 \
  -filter_complex "[1:a]volume=0.08[bg];[0:a][bg]amix=inputs=2:duration=first" \
  voiceover_with_bg.mp3
```

---

## Stage 4: Visual Asset Creation & Video Assembly

This is the most variable stage. Three approaches, from simplest to most polished:

### Approach A: Stock Footage + ffmpeg (Free/cheap, fast)
```bash
# Download stock footage from Pexels (free, no attribution required for most)
# Use the visual descriptions from the script's [VISUAL: ...] tags as search terms

# Assemble clips with ffmpeg
ffmpeg -f concat -safe 0 -i clips.txt -i voiceover_normalized.mp3 \
  -c:v libx264 -c:a aac -shortest output.mp4

# clips.txt format:
# file 'clip1.mp4'
# duration 15
# file 'clip2.mp4'
# duration 20
```

### Approach B: AI Image Generation + Ken Burns (Free-moderate)
Use the [VISUAL: ...] tags from the script as image generation prompts.
```bash
# Generate images via API (if available), then animate with ffmpeg Ken Burns effect
ffmpeg -loop 1 -i image1.png -t 10 \
  -vf "zoompan=z='min(zoom+0.001,1.3)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=250:s=1920x1080" \
  -c:v libx264 -pix_fmt yuv420p segment1.mp4
```

### Approach C: Magic Hour / Remotion (Paid / Code-native)
- **Magic Hour** ($15-39/mo) — GUI-based but handles the hard parts. Good for AI video scenes.
- **Remotion** (Free, React-based) — Programmatic video generation. Steep learning curve but fully automatable.

### Adding Subtitles (CRITICAL for retention)
```bash
# If you generated .vtt from edge-tts:
ffmpeg -i output.mp4 -vf "subtitles=voiceover.vtt:force_style='FontName=Arial,FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Alignment=2'" \
  output_with_subs.mp4

# For word-by-word highlight style (like CapCut auto-captions), use the .vtt timing data
# and render with Remotion or After Effects. ffmpeg can't do highlight-style natively.
```

---

## Stage 5: SEO Optimization

**Tool: Claude (native)**

### Title Optimization
Rules:
- 50-70 characters (YouTube truncates at ~70 on mobile)
- Front-load the keyword. "How Bitcoin Mining Works" not "An Explanation of How Bitcoin Mining Works"
- Include a power word: Shocking, Insane, Actually, Secret, Real Reason, Truth About
- Include a number if listicle: "7 Signs..." not "Signs..."
- Create curiosity gap: Promise info, don't deliver it in the title

Generate 5-10 title variants and rank by predicted CTR.

### Description
```
[First 150 characters are CRITICAL — this shows in search results]
[Restate the hook/value prop]

[Timestamps — these boost SEO and watch time]
0:00 - [Section name]
1:30 - [Section name]
...

[2-3 paragraphs with target keywords woven naturally — 200-500 words total]

[Links, social, related videos]

[Tags as hashtags: #keyword1 #keyword2 #keyword3]
```

### Tags
Generate 15-30 tags:
- 3-5 exact match keywords ("how bitcoin mining works")
- 5-10 broad keywords ("bitcoin", "cryptocurrency", "mining")
- 3-5 competitor channel names (yes, this works)
- 3-5 related topics ("blockchain explained", "crypto for beginners")

### Thumbnail Strategy
Faceless channel thumbnails that work:
- Bold text (3-5 words max) on contrasting background
- One dominant visual element (not cluttered)
- High contrast colors (yellow/black, red/white)
- Emotion or intrigue in the imagery
- 1280x720px, <2MB

Claude can generate thumbnail concepts as text prompts for image generation tools, or use the canvas-design skill if available.

---

## Stage 6: Upload & Scheduling

### YouTube Data API (CLI upload)
```bash
# Install google API client
pip install google-api-python-client google-auth-oauthlib

# First-time OAuth setup required (see references/tool-stack.md)
# After setup, upload via CLI:
python3 upload_video.py \
  --file="output_final.mp4" \
  --title="Your Optimized Title" \
  --description="Your SEO description" \
  --tags="tag1,tag2,tag3" \
  --category="22" \
  --privacy="private"  # Start private, review, then publish
```

### Scheduling Strategy
- **Upload frequency**: 2-3x/week minimum for growth phase. YouTube rewards consistency.
- **Best upload times** (general — varies by niche): Tue-Thu, 2-4 PM EST (catches both US coasts)
- **Batch production**: Script 5-7 videos at once, then batch-produce. More efficient than one-at-a-time.

---

## Full Pipeline Automation (Putting It Together)

For a single video, end-to-end:

```bash
# 1. Claude generates script (user provides topic/angle)
#    Output: script.txt + visual_prompts.txt

# 2. Generate voiceover
edge-tts --voice "en-US-GuyNeural" --rate="+5%" \
  --file script.txt --write-media voiceover.mp3 --write-subtitles voiceover.vtt
ffmpeg -i voiceover.mp3 -af "loudnorm=I=-16:TP=-1.5:LRA=11" voiceover_norm.mp3

# 3. Assemble visuals (stock footage or AI-generated images)
#    Use visual_prompts.txt to source/generate visuals
#    Assemble with ffmpeg concat

# 4. Combine audio + video + subtitles
ffmpeg -i assembled_video.mp4 -i voiceover_norm.mp3 \
  -vf "subtitles=voiceover.vtt:force_style='FontSize=22,Outline=2'" \
  -c:v libx264 -c:a aac -shortest final_output.mp4

# 5. Claude generates title, description, tags
# 6. Upload via YouTube Data API or manually
```

See `scripts/pipeline.sh` for a more complete automation script.

---

## Monetization Requirements Reference

YouTube Partner Program (YPP) requirements as of 2024:
- **Standard monetization**: 1,000 subscribers + 4,000 watch hours (last 12 months) OR 1,000 subscribers + 10 million Shorts views (last 90 days)
- **Fan funding tier** (lower bar): 500 subscribers + 3,000 watch hours OR 3 million Shorts views

Key metrics to track:
- **CTR** (click-through rate): 4-10% is good. Below 4% = fix thumbnails/titles.
- **AVD** (average view duration): 40%+ of video length is good. Below 30% = fix scripting/pacing.
- **RPM** (revenue per mille): Varies wildly by niche. $2-5 entertainment, $8-15 tech, $15-40 finance.

---

## Workflow When User Asks for Help

1. **"I need a video idea"** → Run Stage 1 (niche research / topic ideation)
2. **"Write me a script about X"** → Run Stage 2, output in the structured format
3. **"Help me make a video"** → Run Stages 2-5, outputting files at each stage
4. **"Optimize this for YouTube"** → Run Stage 5 (SEO) on provided content
5. **"Set up my pipeline"** → Walk through tool installation from `references/tool-stack.md`
6. **"Review my channel strategy"** → Analyze their niche, frequency, metrics, and suggest improvements
