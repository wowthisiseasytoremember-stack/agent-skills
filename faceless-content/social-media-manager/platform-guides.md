# Platform-Specific Guides

## TikTok Deep Dive

### Algorithm Mechanics
TikTok's algorithm is the most democratic of any platform — follower count matters less than content quality. Every video gets shown to a small test audience first (~200-500 people). If that cohort engages (watch time, rewatches, shares, comments), it gets pushed to progressively larger audiences.

**What the algorithm measures (in order of importance)**:
1. **Completion rate** — % of viewers who watch to the end. THE most important metric.
2. **Rewatch rate** — Did they loop it? This signals high value.
3. **Shares** — Sends to friends = strongest engagement signal.
4. **Comments** — Quantity AND velocity (comments in first hour matter most).
5. **Likes** — Weakest signal, but still counts.
6. **Follows from video** — "This creator is so good I need to see more."

**Implications for content**:
- Shorter videos complete more often → 15-30s outperforms 60s+ for new accounts
- Loop-friendly content (where the end connects to the beginning) gets rewatched
- Controversial or opinion-based content drives comments
- "Send this to someone who..." drives shares

### TikTok Content Formats That Work for Faceless

1. **Text-on-screen + voiceover**: The bread and butter of faceless TikTok. Stock footage or AI-generated background, text overlay, TTS or custom voiceover.

2. **"Slideshow" style**: Series of images with text + trending audio. Works for listicles, facts, comparisons.

3. **Screen recording + voiceover**: Great for tech/tutorial content. Record a screen demo, narrate over it.

4. **AI-generated scenes**: Use Magic Hour / Runway clips as visuals. Works for story-driven content.

5. **Green screen text**: Use the "green screen" effect with a text post as background. Read/react to the text via voiceover.

### TikTok Growth Tactics
- **Post 1-3x/day** during growth phase. The algorithm rewards volume more than any other platform.
- **Use trending sounds** even in faceless content — just as background. The algorithm boosts videos using trending audio.
- **First 1 second is everything.** If they don't stop scrolling, nothing else matters.
- **Hashtags**: Use 3-5. Mix of niche (#estatesalefinds) + broad (#fyp #viral). Don't overstuff.
- **Post times**: 7-9 AM, 12-1 PM, 7-10 PM in your target audience's timezone. But honestly, content quality >>> post time.
- **Engage in comments on OTHER creators' videos** in your niche. Not spam, genuine comments. This puts your profile in front of their audience.

### TikTok Monetization

**Creator Fund / Creativity Program**:
- Creativity Program Beta (longer videos): $0.50-$1.50 per 1K views. Requires 10K followers + 100K views in last 30 days.
- Original Creator Fund: Being phased out in most regions. Was ~$0.02-0.04/1K views (basically nothing).

**TikTok Shop**:
- Commission on products sold through videos
- Requires 5K followers to access
- Relevant for eBay sellers: can drive traffic if product fits TikTok's demographic

**LIVE Gifts**:
- Viewers send virtual gifts during livestreams
- Not viable for faceless accounts (no face = no LIVE)

**Affiliate/Sponsorship**:
- Once at 10K+ followers, brands reach out
- Typical rates: $200-500 per sponsored post at 50K followers, $500-2000 at 100K+

### TikTok Technical Specs
- Resolution: 1080x1920 (9:16)
- Max file size: 287.6 MB (mobile), 500 MB (desktop)
- Max length: 10 minutes
- Supported formats: MP4, MOV
- Recommended: MP4, H.264, AAC audio

---

## Instagram Deep Dive

### Content Types & Algorithm Behavior

**Reels** (pushed hardest by Instagram):
- Up to 90 seconds
- Shown to non-followers via Explore + Reels tab
- Completion rate is king (same as TikTok)
- Can reuse TikTok content BUT remove the TikTok watermark (Instagram deprioritizes watermarked content)

```bash
# Remove TikTok watermark by cropping (watermark is usually top-center)
ffmpeg -i tiktok_video.mp4 -vf "crop=in_w:in_h-120:0:60" instagram_reel.mp4
```

**Carousels** (highest engagement rate of any format):
- Up to 10 slides
- Users spend more time swiping = higher dwell time = algorithm boost
- Best for: educational content, step-by-step, listicles
- Optimal: 7-10 slides. Less than 5 feels incomplete.

**Stories** (for engaged followers only):
- 24-hour expiry (unless Highlighted)
- Not for reach — for deepening connection with existing followers
- Use polls, questions, quizzes to drive engagement
- 5-7 stories/day is ideal. More than 10 = dropoff.

**Feed Posts** (declining in importance):
- Single image with long caption
- Still useful for "evergreen" content that lives on your grid
- Algorithm heavily favors Reels and Carousels over static images now

### Instagram Faceless Strategy
Instagram is harder to grow faceless than TikTok because the platform was built around personal brands and aesthetics. Workarounds:

- **Branded visual identity**: Pick a color palette, font style, and template. Every post should be instantly recognizable. Tools: Canva templates, or Claude + canvas-design skill.
- **Educational niche accounts**: @facts, @science, @motivation-style accounts thrive faceless.
- **Meme/humor accounts**: High growth potential but harder to monetize.
- **Quote/inspiration accounts**: Easy to produce, moderate growth, good for affiliate.

### Instagram Monetization
- **Reels Bonuses**: Invite-only. $100-1,000/month when active. Instagram keeps turning this on/off.
- **Affiliate links**: Link in bio → Linktree → product links. Typical conversion: 1-3% of link clicks.
- **Sponsored posts**: Similar rates to TikTok. $100-300 at 10K followers, scaling up.
- **Instagram Shop**: If selling physical products (relevant for eBay crossover).

---

## Twitter/X Deep Dive

### Algorithm & Content Strategy

**What gets reach on Twitter**:
1. Threads (5-15 tweets) — by far the highest reach format
2. Tweets with images/video attached
3. Quote tweets with added commentary
4. Plain text tweets with strong hooks

**What dies on Twitter**:
1. Links in tweets (algorithm suppresses external links — put links in replies instead)
2. Threads with no hook in tweet 1
3. Engagement bait without substance ("Like if you agree!")

### Thread Writing for Growth

**Thread Formula**:
```
Tweet 1 (HOOK): [Bold claim]. Here's what I learned: 🧵
Tweet 2: [Context / why this matters]
Tweet 3-N: [One insight per tweet, each self-contained]
Final tweet: [Summary + CTA: "Follow @handle for more [topic]"]
Reply to final tweet: [Link to your product/site — keeps it off the main thread]
```

**High-performing thread angles**:
- "I studied [100 examples of X]. Here's what I found."
- "The [topic] playbook nobody shares for free."
- "[X] mistakes I made so you don't have to."
- "How [person/company] achieved [result] (breakdown)."

### Twitter Monetization
- **Ads Revenue Share**: Available to X Premium subscribers ($8/mo). Requires 5M organic impressions in last 3 months. Typical payout: $2-8 per 1M impressions.
- **Affiliate**: Higher intent clicks than TikTok/Instagram. Tech and finance niches convert well.
- **Lead generation**: For app launches, Twitter is strong for B2B and tech-savvy consumer audiences.

### Twitter API Costs
- **Free tier**: Read-only, very limited
- **Basic tier**: $100/month — 50K tweets read, 1,667 tweets post per month
- **Pro tier**: $5,000/month — overkill for most use cases

For scheduling tweets via CLI, the Basic tier is the minimum. Alternatively, use a free scheduler (Buffer, Typefully) and skip the API.

---

## LinkedIn Deep Dive

### When to Use LinkedIn
- Launching a B2B product or professional tool
- Building authority in a professional domain
- Driving traffic to a SaaS or business product
- NOT useful for: faceless entertainment, consumer products, eBay store promotion

### What Works on LinkedIn
- **Personal stories with professional lessons** — "I got fired and here's what I learned" gets 10x the engagement of "5 business tips"
- **Contrarian takes** — "Unpopular opinion: [industry belief] is wrong because..."
- **Data-driven posts** — Share specific numbers from your experience
- **Carousel documents** — Upload a PDF that becomes a swipeable carousel. These get massive reach.

### LinkedIn Post Anatomy
```
[First line — this shows before "See more." Make it count.]
[Blank line]
[Story or insight — 1,000-1,500 characters optimal]
[Blank line]
[Key takeaway in bold terms]
[Blank line]
[Question to drive comments]
[Blank line]
[3-5 hashtags: #industryterm #broadertopic]
```

### LinkedIn Algorithm Notes
- Posts with external links get suppressed. Put links in FIRST COMMENT, not the post.
- Dwell time (how long people spend reading) is a major ranking signal.
- Comments from connections of your connections expand reach (network effect).
- Posting frequency sweet spot: 3-5x/week. More than daily can hurt.

---

## Pinterest Deep Dive

### Why Pinterest Matters (Often Overlooked)
Pinterest is a SEARCH ENGINE disguised as a social platform. Content has a shelf life of 3-6 months vs hours on other platforms. For evergreen niches, it's a traffic machine.

### Pinterest Strategy for Faceless Content
- **Create pins for every YouTube video**: Take the thumbnail, add text overlay, link to video.
- **Idea Pins** (multi-page, no link): Good for reach but don't drive traffic directly.
- **SEO matters here**: Keyword-optimize pin titles and descriptions like you would a blog post.

### Pinterest Specs
- Pin dimensions: 1000x1500 (2:3 ratio) optimal
- Idea Pins: 1080x1920 (9:16), up to 20 pages
- Include text overlay on every pin — they're displayed small in feeds

---

## Platform Priority Recommendations

### For App Launch (Consumer App)
1. TikTok (reach) → 2. Twitter (tech audience) → 3. Instagram (credibility) → 4. LinkedIn (if B2B angle)

### For App Launch (B2B / SaaS)
1. Twitter (decision makers) → 2. LinkedIn (authority) → 3. YouTube (tutorials) → 4. TikTok (optional)

### For Faceless Monetization
1. YouTube long-form (highest RPM) → 2. TikTok (fastest growth) → 3. YouTube Shorts (subscriber funnel) → 4. Instagram Reels (bonus income)

### For eBay Store Traffic
1. TikTok (haul/find content) → 2. Instagram Reels (same content) → 3. Pinterest (evergreen product pins) → 4. eBay Promoted Listings (paid, but stays in-platform)
