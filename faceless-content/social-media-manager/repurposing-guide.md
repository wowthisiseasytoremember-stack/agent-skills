# Content Repurposing Guide

## The Repurposing Pipeline

### Input → Output Matrix

| Source Content | TikTok | Reel | Short | Thread | Carousel | LinkedIn | Pin |
|---------------|--------|------|-------|--------|----------|----------|-----|
| YouTube video | Clip 3-5 moments | Same clips, no watermark | Best 60s clip | Key points as text | Visual summary | Professional angle | Thumbnail + link |
| Blog post | Narrate key point | Narrate key point | Narrate hook | Adapt as thread | Slide per section | Share insight | Infographic |
| Twitter thread | Narrate thread | Narrate thread | Narrate hook | Already done | Adapt to slides | Cross-post | Quote graphic |
| Podcast episode | Clip best moment | Same clip | Same clip | Key takeaways | Guest quotes | Episode summary | Audiogram |

---

## YouTube → Short-Form Clips

### Identifying Clip-Worthy Moments

When repurposing a YouTube video, look for these patterns in the script:

1. **The Hook** (always clip-worthy) — First 30-60 seconds usually works standalone
2. **"Wait, really?" moments** — Any surprising fact, stat, or revelation
3. **The best analogy** — A single point explained perfectly in 30-60 seconds
4. **Controversy/hot takes** — Opinion moments that drive comments
5. **The climax** — The payoff of the whole video, if it makes sense without context

### Clip Extraction Workflow

```bash
# Step 1: Identify timestamps (from script or by reviewing video)
# Step 2: Extract clips

# Basic extraction (keeps original aspect ratio)
ffmpeg -i youtube_video.mp4 -ss 00:03:22 -to 00:04:15 \
  -c:v libx264 -c:a aac clip_01.mp4

# Convert 16:9 → 9:16 with blur background (most common approach)
ffmpeg -i youtube_video.mp4 -ss 00:03:22 -to 00:04:15 \
  -filter_complex "\
    [0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30[bg];\
    [0:v]scale=1080:-2[fg];\
    [bg][fg]overlay=(W-w)/2:(H-h)/2\
  " \
  -c:v libx264 -c:a aac clip_01_vertical.mp4

# Convert 16:9 → 9:16 with center crop (cleaner, loses edges)
ffmpeg -i youtube_video.mp4 -ss 00:03:22 -to 00:04:15 \
  -vf "crop=ih*9/16:ih,scale=1080:1920" \
  -c:v libx264 -c:a aac clip_01_cropped.mp4

# Add captions from .vtt (adjust timestamps relative to clip start)
ffmpeg -i clip_01_vertical.mp4 \
  -vf "subtitles=clip_subs.vtt:force_style='FontName=Arial Bold,FontSize=28,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=3,Alignment=2,MarginV=150'" \
  -c:v libx264 -c:a aac clip_01_captioned.mp4
```

### Platform-Specific Adjustments

**TikTok version**:
- Can include trending sound as background (boosts algorithm)
- Add text hook on first frame
- End with loop potential or CTA

**Instagram Reel version**:
- REMOVE any TikTok watermark (Instagram suppresses these)
- Slightly different caption style (more hashtags, less casual)
- Can be identical to TikTok content otherwise

**YouTube Short version**:
- Add end screen text: "Watch the full video →" 
- Include #Shorts in title
- Use the hook/best moment, not the same clip as TikTok (different audiences)

---

## YouTube → Twitter Thread

### Extraction Process

1. Take the YouTube script
2. Identify the 5-10 most interesting/useful points
3. Write each as a standalone tweet (≤280 chars)
4. Add a hook as tweet 1 and a CTA as the final tweet

### Template

From a script about "How Bitcoin Mining Works":

```
Tweet 1: Bitcoin mining doesn't work the way most people think.

Here's what's actually happening — explained so anyone can understand it: 🧵

Tweet 2: First, forget the word "mining." Nothing is being dug up.

Miners are actually competing to solve a math puzzle. The first one to solve it gets paid in new Bitcoin.

Tweet 3: The puzzle itself is simple: find a number that, when combined with the transaction data and run through a hash function, produces a result starting with a certain number of zeros.

Tweet 4: The catch? There's no shortcut. You can only guess and check. Billions of times per second.

That's what all those mining rigs are doing — making random guesses as fast as possible.

[... continue for each key point ...]

Tweet 10: TL;DR:
→ Mining = competitive guessing game
→ More miners = harder puzzles
→ Energy cost is the real bottleneck
→ You probably shouldn't mine from your apartment

Follow @handle for more breakdowns like this.
```

---

## YouTube → Instagram Carousel

### Extraction Process

1. Take the YouTube script
2. Identify 7-10 key points or steps
3. Write each as a short text block (1-3 sentences)
4. Design each as a slide with consistent visual template

### Slide Content Template

```
Slide 1 (HOOK):
  [Large text]: "How Bitcoin Mining ACTUALLY Works"
  [Subtext]: "Swipe to learn →"
  [Visual]: Bold colors, contrasting background

Slide 2 (CONTEXT):
  [Text]: "Most people think mining means digging up digital coins. The reality is way more interesting."

Slide 3-8 (KEY POINTS):
  [Header]: Point title
  [Body]: 1-2 sentences
  [Visual]: Supporting icon or simple illustration

Slide 9 (SUMMARY):
  [Text]: "Key takeaways:" + 3-4 bullet points

Slide 10 (CTA):
  [Text]: "Found this useful? Save it for later."
  [Subtext]: "Follow @handle for more breakdowns"
```

### Carousel Design Via CLI

For generating carousel images without Canva/GUI:

```bash
# Use ImageMagick to generate slides from text
convert -size 1080x1350 xc:"#1a1a2e" \
  -font "Arial-Bold" -pointsize 60 -fill white \
  -gravity center -annotate +0-200 "How Bitcoin Mining" \
  -annotate +0-100 "ACTUALLY Works" \
  -font "Arial" -pointsize 36 -fill "#aaaaaa" \
  -annotate +0+50 "Swipe to learn →" \
  slide_01.png

# Batch-generate slides from a text file
# (More practical: use Claude + canvas-design skill or a React artifact)
```

---

## Batch Repurposing Script

For processing multiple clips from one YouTube video:

```bash
#!/bin/bash
# batch_repurpose.sh
# Usage: ./batch_repurpose.sh <video_file> <timestamps_file>
#
# timestamps_file format (one clip per line):
# START,END,TITLE
# 00:01:15,00:02:00,hook_the_surprising_truth
# 00:04:30,00:05:15,best_analogy_about_mining
# 00:08:00,00:08:45,mind_blowing_stat

VIDEO="$1"
TIMESTAMPS="$2"
OUTPUT_DIR="./repurposed_$(date +%Y%m%d)"

mkdir -p "$OUTPUT_DIR"/{tiktok,reels,shorts}

while IFS=, read -r START END TITLE; do
  echo "Processing: $TITLE ($START → $END)"
  
  # TikTok version (blur background)
  ffmpeg -y -i "$VIDEO" -ss "$START" -to "$END" \
    -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30[bg];[0:v]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" \
    -c:v libx264 -c:a aac "$OUTPUT_DIR/tiktok/${TITLE}.mp4" 2>/dev/null
  
  # Reels version (identical but separate file for tracking)
  cp "$OUTPUT_DIR/tiktok/${TITLE}.mp4" "$OUTPUT_DIR/reels/${TITLE}.mp4"
  
  # Shorts version (center crop, slightly different framing)
  ffmpeg -y -i "$VIDEO" -ss "$START" -to "$END" \
    -vf "crop=ih*9/16:ih,scale=1080:1920" \
    -c:v libx264 -c:a aac "$OUTPUT_DIR/shorts/${TITLE}.mp4" 2>/dev/null
  
  echo "  ✓ Done"
done < "$TIMESTAMPS"

echo ""
echo "Output: $OUTPUT_DIR"
echo "  tiktok/  — $(ls "$OUTPUT_DIR/tiktok/" | wc -l) clips"
echo "  reels/   — $(ls "$OUTPUT_DIR/reels/" | wc -l) clips"
echo "  shorts/  — $(ls "$OUTPUT_DIR/shorts/" | wc -l) clips"
```

---

## Content Calendar Generation

When Claude generates a content calendar, use this format:

```
WEEK OF: [Date]
ANCHOR CONTENT: [YouTube video title]
SCRIPT WORD COUNT: [X words / Y minutes]

DERIVATIVES:
├── TikTok 1: [Clip title] (0:XX-0:XX from anchor) — Post [day] [time]
├── TikTok 2: [Clip title] (0:XX-0:XX from anchor) — Post [day] [time]
├── TikTok 3: [Clip title] (0:XX-0:XX from anchor) — Post [day] [time]
├── Reel 1: [Same as TikTok 1, reformatted] — Post [day] [time]
├── Reel 2: [Same as TikTok 2, reformatted] — Post [day] [time]
├── YouTube Short: [Best 60s clip] — Post [day] [time]
├── Twitter Thread: [Topic angle] (7 tweets) — Post [day] [time]
├── LinkedIn Post: [Professional angle] — Post [day] [time]
├── Instagram Carousel: [Visual summary, 8 slides] — Post [day] [time]
└── Pinterest Pin: [Thumbnail + link] — Post [day]

ENGAGEMENT TASKS:
├── Reply to comments on all posts (15 min/day)
├── Comment on 10 niche creators' posts (10 min/day)
└── Check analytics, note what's working (5 min/day)

TOTAL ACTIVE TIME: ~[X] hours this week
```

---

## Quality Checklist Before Posting

Run through this for every piece of content before it goes live:

**All platforms**:
- [ ] First 1-3 seconds demand attention (would YOU stop scrolling?)
- [ ] Captions/text are readable on mobile
- [ ] Audio levels are consistent (no sudden loud/quiet)
- [ ] No copyrighted music unless properly licensed
- [ ] CTA is clear (follow, comment, save, or link)
- [ ] Hashtags are relevant (not spammy)

**Video-specific**:
- [ ] 9:16 aspect ratio for vertical platforms
- [ ] No black bars or awkward cropping
- [ ] No watermarks from other platforms
- [ ] Subtitles are accurate and timed correctly

**Cross-posted content**:
- [ ] Platform-specific caption (don't copy-paste TikTok caption to LinkedIn)
- [ ] Hashtag strategy matches platform norms
- [ ] Link placement follows platform rules (bio vs comment vs post)
