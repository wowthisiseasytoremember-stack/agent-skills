# Tool Stack Reference

## Overview

This document covers setup, configuration, and cost comparison for every tool in the faceless YouTube pipeline. Organized by pipeline stage.

---

## Tier 1: Free / CLI-Native (No API Keys Required)

### edge-tts (Voiceover)
- **Cost**: Free
- **Quality**: 7/10 (surprisingly good for free)
- **Setup**:
```bash
pip install edge-tts
```
- **Best voices for YouTube**:
  - `en-US-GuyNeural` — Warm, natural male. Best all-rounder.
  - `en-US-AndrewNeural` — Deeper, authoritative. Good for finance/tech.
  - `en-US-JennyNeural` — Clear, conversational female.
  - `en-US-AriaNeural` — Energetic female. Good for listicles.
  - `en-GB-RyanNeural` — British male. Good for history/documentary tone.
- **Pro tip**: Use `--rate="+5%"` to `"+15%"` for more energetic pacing. YouTube audiences prefer slightly faster delivery.
- **Limitations**: No voice cloning. Limited emotional range. Occasional weird pauses on punctuation.

### ffmpeg (Video Assembly / Audio Processing)
- **Cost**: Free
- **Setup**: Usually pre-installed on Linux. Otherwise:
```bash
sudo apt install ffmpeg
```
- **Key commands for YouTube pipeline**:
```bash
# Audio normalization (ALWAYS do this)
ffmpeg -i input.mp3 -af "loudnorm=I=-16:TP=-1.5:LRA=11" output.mp3

# Concatenate video clips
ffmpeg -f concat -safe 0 -i filelist.txt -c:v libx264 -c:a aac output.mp4

# Ken Burns effect on still images (zoom + pan)
ffmpeg -loop 1 -i image.png -t 10 \
  -vf "zoompan=z='min(zoom+0.001,1.3)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=250:s=1920x1080" \
  -c:v libx264 -pix_fmt yuv420p output.mp4

# Add subtitles (burn in)
ffmpeg -i video.mp4 -vf "subtitles=subs.vtt:force_style='FontName=Arial,FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2'" output.mp4

# Overlay background music at low volume
ffmpeg -i voice.mp3 -i music.mp3 \
  -filter_complex "[1:a]volume=0.08[bg];[0:a][bg]amix=inputs=2:duration=first" mixed.mp3

# Scale to 1080p (YouTube preferred)
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:-1:-1:black" output.mp4
```

### yt-dlp (Competitive Research)
- **Cost**: Free
- **Setup**:
```bash
pip install yt-dlp
```
- **Research commands**:
```bash
# List all videos from a channel with view counts
yt-dlp --flat-playlist --print "%(title)s | %(view_count)s | %(upload_date)s | %(duration)s" \
  "https://www.youtube.com/@ChannelName/videos" | head -50

# Download auto-generated subtitles (great for studying competitor scripts)
yt-dlp --write-auto-sub --sub-lang en --skip-download "VIDEO_URL"

# Download thumbnail
yt-dlp --write-thumbnail --skip-download "VIDEO_URL"

# Get video metadata as JSON
yt-dlp --dump-json "VIDEO_URL" | python3 -m json.tool
```

### Pexels API (Stock Footage)
- **Cost**: Free (API key required but no payment)
- **Setup**: Register at pexels.com/api, get API key
```bash
# Search for stock videos
curl -H "Authorization: YOUR_PEXELS_KEY" \
  "https://api.pexels.com/videos/search?query=city+aerial+night&per_page=5"

# Download with wget/curl from the returned URLs
```
- **License**: Free for commercial use, no attribution required (but appreciated).
- **Alternatives**: Pixabay API (also free), Coverr.co (free, no API)

---

## Tier 2: Paid CLI-Capable Tools

### ElevenLabs (Voiceover — Premium)
- **Cost**: $5/mo (10K chars) | $22/mo (100K chars) | $99/mo (500K chars)
- **Quality**: 9/10
- **Setup**:
```bash
pip install elevenlabs
export ELEVEN_API_KEY="your_key_here"
```
- **Usage**:
```python
from elevenlabs import generate, save, set_api_key
import os

set_api_key(os.environ["ELEVEN_API_KEY"])

# A 2,000-word script ≈ 12,000 characters
audio = generate(
    text=open("script.txt").read(),
    voice="Adam",  # or any cloned/preset voice
    model="eleven_monolingual_v1"
)
save(audio, "voiceover.mp3")
```
- **Pro tip**: The $22/mo plan covers ~8 videos/month at 12K chars each. Good ROI if the channel makes any ad revenue.
- **Voice cloning**: Available on $22+ plans. Upload 1-30 min of clean audio to create a custom voice.

### Kokoro TTS (Free, Local, High Quality)
- **Cost**: Free (open source)
- **Quality**: 8/10 (approaching ElevenLabs)
- **Requirement**: Works on CPU but slow. GPU recommended.
- **Setup**:
```bash
pip install kokoro-onnx soundfile
# Download model files (see https://github.com/remsky/Kokoro-FastAPI)
```
- **Best for**: Users who want ElevenLabs-tier quality without monthly costs and have decent hardware.

### Magic Hour (AI Video Generation)
- **Cost**: $15/mo (basic) | $39/mo (pro)
- **Quality**: 7-8/10 for AI-generated scenes
- **CLI**: No native CLI. GUI-based workflow.
- **When to use**: When stock footage won't cut it and you need AI-generated scenes (sci-fi, historical recreations, abstract concepts).
- **Alternative**: RunwayML ($15/mo), Kling AI, Pika Labs

---

## Tier 3: GUI Tools (Manual Steps)

### CapCut (Video Editing)
- **Cost**: Free (with Pro at $8-15/mo)
- **CLI**: No. Desktop/mobile app only.
- **Why it's still worth using**: Auto-captions are the best in the business. The word-by-word highlight effect that keeps retention high is hard to replicate with ffmpeg alone.
- **When to use**: Final polish pass. Add auto-captions, transitions, sound effects.
- **Workflow**: Do 90% in ffmpeg/CLI, import into CapCut for the last 10%.

### Canva (Thumbnails)
- **Cost**: Free (Pro at $13/mo)
- **CLI**: No, but has templates specifically for YouTube thumbnails.
- **Alternative**: Use Claude + canvas-design skill to generate thumbnail concepts, then render via code.

---

## Cost Comparison Matrix

| Workflow          | Monthly Cost | Quality | Automation Level |
|-------------------|-------------|---------|-----------------|
| Full free stack   | $0          | 6-7/10  | 85% automated   |
| edge-tts + ElevenLabs | $22    | 8/10    | 85% automated   |
| ElevenLabs + Magic Hour | $37-61 | 8-9/10 | 70% automated  |
| Full paid stack   | $60-100     | 9/10    | 75% automated   |

The "full free stack" (Claude + edge-tts + ffmpeg + Pexels) is genuinely viable for starting out. Upgrade voiceover first (biggest quality impact per dollar), then video generation.

---

## YouTube Data API Setup (Upload Automation)

This is the most complex setup but enables fully automated uploading.

### Step 1: Google Cloud Console
1. Go to console.cloud.google.com
2. Create a new project
3. Enable "YouTube Data API v3"
4. Create OAuth 2.0 credentials (Desktop app type)
5. Download the `client_secrets.json` file

### Step 2: First-time OAuth
```python
import google_auth_oauthlib.flow

flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    'client_secrets.json',
    scopes=['https://www.googleapis.com/auth/youtube.upload']
)
credentials = flow.run_local_server(port=8080)

# Save credentials for reuse
import pickle
with open('youtube_credentials.pkl', 'wb') as f:
    pickle.dump(credentials, f)
```

### Step 3: Upload Script
```python
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

with open('youtube_credentials.pkl', 'rb') as f:
    credentials = pickle.load(f)

youtube = build('youtube', 'v3', credentials=credentials)

request = youtube.videos().insert(
    part='snippet,status',
    body={
        'snippet': {
            'title': 'Your Video Title',
            'description': 'Your SEO description',
            'tags': ['tag1', 'tag2', 'tag3'],
            'categoryId': '22'  # People & Blogs
        },
        'status': {
            'privacyStatus': 'private',  # Always upload private first
            'publishAt': '2024-01-15T14:00:00Z',  # Schedule publish
            'selfDeclaredMadeForKids': False
        }
    },
    media_body=MediaFileUpload('final_video.mp4', chunksize=-1, resumable=True)
)

response = request.execute()
print(f"Uploaded: https://youtube.com/watch?v={response['id']}")
```

### Category IDs Reference
- 1: Film & Animation
- 10: Music
- 15: Pets & Animals
- 17: Sports
- 20: Gaming
- 22: People & Blogs (default for most faceless channels)
- 24: Entertainment
- 25: News & Politics
- 26: Howto & Style
- 27: Education
- 28: Science & Technology

---

## Free Background Music Sources

All of these are safe for YouTube monetization:
- **YouTube Audio Library** (studio.youtube.com → Audio Library) — Free, pre-cleared
- **Pixabay Music** (pixabay.com/music) — Free, no attribution required
- **Uppbeat** (uppbeat.io) — Free tier with attribution, paid without
- **Epidemic Sound** ($15/mo) — Best quality, fully cleared, worth it once monetized
