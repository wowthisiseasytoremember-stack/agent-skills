# n8n Setup Guide

## Overview

n8n is a free, self-hosted workflow automation tool. It's the backbone of the auto-posting pipeline. It runs on the Dell OptiPlex (already configured as an always-on server) and watches the content queue for approved posts.

---

## Installation (Dell OptiPlex / Ubuntu)

### Option A: Docker (Recommended)
```bash
# Pull and run n8n
docker run -d --restart unless-stopped \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  -v /home/user/content-queue:/content-queue \
  -e GENERIC_TIMEZONE="America/Los_Angeles" \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=your_password_here \
  n8nio/n8n

# Access at http://DELL_IP:5678
# From local network: http://192.168.x.x:5678
```

### Option B: npm (If Docker isn't available)
```bash
npm install n8n -g
export N8N_BASIC_AUTH_ACTIVE=true
export N8N_BASIC_AUTH_USER=admin
export N8N_BASIC_AUTH_PASSWORD=your_password_here

# Run as background service
nohup n8n start &

# Or create a systemd service:
sudo tee /etc/systemd/system/n8n.service << 'EOF'
[Unit]
Description=n8n workflow automation
After=network.target

[Service]
Type=simple
User=your_username
Environment=N8N_BASIC_AUTH_ACTIVE=true
Environment=N8N_BASIC_AUTH_USER=admin
Environment=N8N_BASIC_AUTH_PASSWORD=your_password_here
Environment=GENERIC_TIMEZONE=America/Los_Angeles
ExecStart=/usr/local/bin/n8n start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable n8n
sudo systemctl start n8n
```

---

## Core Workflows

### Workflow 1: Queue Watcher (The Heart)

This runs every 5 minutes and checks for content that's ready to post.

**n8n workflow steps:**
```
[Cron Trigger: */5 * * * *]
    │
    ▼
[Read Directory: /content-queue/approved/]
    │
    ▼
[For Each File:]
    │
    ├─▶ [Read JSON file]
    │
    ├─▶ [Check: scheduled_at <= now?]
    │       │
    │       No ──▶ [Skip]
    │       │
    │       Yes ──▶ [Move to /posting/]
    │               │
    │               ▼
    │        [Route by platform:]
    │               │
    │               ├── youtube ──▶ [YouTube Upload Subworkflow]
    │               ├── twitter ──▶ [Twitter Post Subworkflow]
    │               ├── instagram ──▶ [Instagram Post Subworkflow]
    │               ├── tiktok ──▶ [TikTok Manual Queue + Notification]
    │               └── linkedin ──▶ [LinkedIn Post Subworkflow]
    │
    ▼
[On Success: Move to /posted/, update JSON with post_url]
[On Failure: Move to /failed/, log error, send notification]
```

### n8n JSON Import (Queue Watcher)

Paste this into n8n's "Import from JSON" to get the base workflow:

```json
{
  "name": "Content Autopilot - Queue Watcher",
  "nodes": [
    {
      "name": "Cron Trigger",
      "type": "n8n-nodes-base.cron",
      "position": [250, 300],
      "parameters": {
        "triggerTimes": {
          "item": [{ "mode": "everyX", "value": 5, "unit": "minutes" }]
        }
      }
    },
    {
      "name": "List Approved Files",
      "type": "n8n-nodes-base.readBinaryFiles",
      "position": [450, 300],
      "parameters": {
        "fileSelector": "/content-queue/approved/*.json"
      }
    },
    {
      "name": "Parse & Check Schedule",
      "type": "n8n-nodes-base.function",
      "position": [650, 300],
      "parameters": {
        "functionCode": "const items = [];\nfor (const item of $input.all()) {\n  const content = JSON.parse(item.binary.data.data.toString('utf8'));\n  const scheduledAt = new Date(content.scheduled_at);\n  if (scheduledAt <= new Date()) {\n    items.push({ json: content });\n  }\n}\nreturn items;"
      }
    },
    {
      "name": "Route by Platform",
      "type": "n8n-nodes-base.switch",
      "position": [850, 300],
      "parameters": {
        "dataPropertyName": "platform",
        "rules": {
          "rules": [
            { "value": "youtube" },
            { "value": "twitter" },
            { "value": "instagram" },
            { "value": "tiktok" }
          ]
        }
      }
    }
  ]
}
```

**Note**: This is a skeleton. Each platform output connects to its own subworkflow (below).

---

### Workflow 2: YouTube Upload

```
[Receive from Queue Watcher]
    │
    ▼
[Read video file from content.video_file path]
    │
    ▼
[YouTube API: videos.insert]
    │  Parameters:
    │    title: content.seo.title
    │    description: content.seo.description
    │    tags: content.seo.tags
    │    categoryId: "22"
    │    privacyStatus: "public" (or "private" for review)
    │    publishAt: content.scheduled_at (if scheduling future)
    │
    ▼
[Update queue JSON: status="posted", post_url=response.url]
    │
    ▼
[Move file to /posted/]
```

**YouTube API Credentials in n8n:**
1. In n8n, go to Credentials → New → Google OAuth2
2. Use the same client_secrets.json from the YouTube Data API setup (see faceless-youtube skill)
3. Authorize with your channel's Google account
4. Select scope: `https://www.googleapis.com/auth/youtube.upload`

### Workflow 3: Twitter Post

```
[Receive from Queue Watcher]
    │
    ▼
[Check content_type:]
    │
    ├── "tweet" ──▶ [Twitter API: POST /2/tweets]
    │                  body: { "text": content.content.caption }
    │
    ├── "thread" ──▶ [Loop through content.content.tweets]
    │                  First: POST /2/tweets → get tweet_id
    │                  Rest: POST /2/tweets with reply.in_reply_to_tweet_id = previous_id
    │
    └── "tweet_with_media" ──▶ [Upload media first, then tweet with media_ids]
    │
    ▼
[Update queue JSON, move to /posted/]
```

**Twitter API Setup in n8n:**
1. Apply for Twitter API access at developer.twitter.com
2. Get API Key, API Secret, Access Token, Access Token Secret
3. In n8n: Credentials → New → Twitter OAuth2
4. Note: Free tier = read-only. Basic ($100/mo) = 1,667 posts/month.

**Free Alternative: Browser Automation**
If $100/mo is too steep, n8n can use Puppeteer/Playwright to post via the browser:
```
[Receive from Queue Watcher]
    │
    ▼
[Puppeteer: Open twitter.com, log in (saved session)]
    │
    ▼
[Puppeteer: Click compose, type content, click post]
    │
    ▼
[Extract post URL from redirect]
```
This is fragile (breaks when Twitter changes their UI) but free.

### Workflow 4: Instagram Post (Business Account)

```
[Receive from Queue Watcher]
    │
    ▼
[Check content_type:]
    │
    ├── "reel" ──▶ [Upload video to hosting URL first (S3/GDrive/public URL)]
    │               │
    │               ▼
    │              [Graph API: POST /{ig-user-id}/media]
    │                media_type: "REELS"
    │                video_url: hosted_url
    │                caption: content.content.caption
    │               │
    │               ▼
    │              [Graph API: POST /{ig-user-id}/media_publish]
    │                creation_id: response.id
    │
    ├── "carousel" ──▶ [Upload each image, create container, publish]
    │
    └── "image" ──▶ [Upload image, create, publish]
    │
    ▼
[Update queue JSON, move to /posted/]
```

**Instagram API Requirements:**
- Instagram Business or Creator account (free to switch)
- Facebook Page linked to Instagram account
- Meta App with Instagram Graph API permissions
- Access token with `instagram_content_publish` scope

**Setup steps:**
1. Convert Instagram to Business account (Settings → Account → Switch to Business)
2. Create a Facebook Page (can be minimal)
3. Link Instagram to Facebook Page
4. Go to developers.facebook.com → Create App → Add Instagram Graph API
5. Generate long-lived access token
6. In n8n: Credentials → New → Meta/Facebook OAuth2

### Workflow 5: TikTok (Manual Queue + Notification)

TikTok has no reliable posting API for individual creators. The realistic approach:

```
[Receive from Queue Watcher]
    │
    ▼
[Move video file to /content-queue/tiktok-ready/]
    │
    ▼
[Send notification: "TikTok post ready: {title}. Video at: {path}. Caption: {caption}"]
    │   Via: Email, Slack, Pushover, or Telegram bot
    │
    ▼
[Update queue JSON: status="awaiting_manual_post"]
```

**The manual step**: Open the notification, grab the video file and caption, post via TikTok app. Takes ~60 seconds per post. Not ideal but TikTok actively kills automated posting.

**Semi-automated option**: Use a scheduling tool like Later or Buffer that has TikTok publishing (requires their paid plans + TikTok Business account).

---

### Workflow 6: Daily Digest

```
[Cron Trigger: 8:00 AM daily]
    │
    ▼
[Read /posted/ directory: files from yesterday]
    │
    ▼
[Read /approved/ directory: files scheduled for today]
    │
    ▼
[Read /failed/ directory: any failures]
    │
    ▼
[Compose digest message:]
    "📊 Content Autopilot Daily Digest
    
    Yesterday: {N} posts published
    ✅ YouTube: {title} — {url}
    ✅ Twitter: {title} — {url}
    ⏳ TikTok: {title} — awaiting manual post
    
    Today: {N} posts scheduled
    • 12:00 PM — TikTok: {title}
    • 2:00 PM — YouTube: {title}
    • 3:00 PM — Twitter thread: {title}
    
    ❌ Failures: {N}
    • Instagram: {title} — Error: token expired"
    │
    ▼
[Send via preferred channel: Email / Slack / Pushover / Telegram]
```

---

## Notification Setup

Pick one (or multiple):

### Pushover ($5 one-time, best for phone notifications)
```
n8n HTTP Request node:
POST https://api.pushover.net/1/messages.json
body: {
  token: "APP_TOKEN",
  user: "USER_KEY",
  message: "Content ready to post: ...",
  title: "Content Autopilot"
}
```

### Telegram Bot (Free)
```bash
# Create bot via @BotFather on Telegram
# Get your chat_id by messaging @userinfobot

# n8n has a native Telegram node:
# Action: Send Message
# Chat ID: your_chat_id
# Text: notification message
```

### Email (Free via Gmail SMTP)
n8n has a native Email node. Use Gmail app password.

---

## Maintenance

### Weekly
- Review `/failed/` directory for persistent issues
- Check API token expiration dates (Instagram tokens expire every 60 days)
- Verify n8n is running: `docker ps` or `systemctl status n8n`

### Monthly
- Archive old posts: move `/posted/` files older than 30 days to `/archive/`
- Review posting analytics (if tracking in queue JSON)
- Rotate any API credentials approaching expiration

### Auto-Cleanup Script
```bash
#!/bin/bash
# cleanup.sh — Run via cron monthly
# Move posted items older than 30 days to archive

find /content-queue/posted/ -name "*.json" -mtime +30 -exec mv {} /content-queue/archive/ \;
echo "Archived $(find /content-queue/archive/ -name "*.json" -newer /tmp/cleanup_marker | wc -l) files"
touch /tmp/cleanup_marker
```

Add to cron: `0 0 1 * * /path/to/cleanup.sh`

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Posts not going out | n8n stopped | `docker restart n8n` or `systemctl restart n8n` |
| YouTube upload fails | OAuth token expired | Re-authorize in n8n credentials |
| Instagram publish fails | Access token expired | Refresh token (expires every 60 days) |
| Twitter thread out of order | API rate limit | Add 2s delay between thread tweets in n8n |
| TikTok notification not received | Notification service down | Check Pushover/Telegram bot status |
| Queue files piling up in drafts | Nothing approved | Remind user to review and approve |
| Wrong timezone on posts | n8n timezone misconfigured | Set GENERIC_TIMEZONE env variable |
