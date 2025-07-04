# AI Twitter Motivational Quote Bot

Generate and post AI-powered motivational quotes to Twitter automatically.

## Features

- 🤖 AI-generated quotes using Google Gemini (FREE)
- 🐦 Auto-post to Twitter (FREE - 1,500 tweets/month)
- 🔄 Duplicate prevention
- ⏰ Scheduled or manual posting

## Quick Setup

### 1. Install packages

```bash
pip install -r requirements.txt
```

### 2. Get FREE API keys

- **Gemini API**: https://aistudio.google.com/app/apikey
- **Twitter API**: https://developer.twitter.com/en/portal/dashboard

### 3. Setup environment

Copy `.env.example` to `.env` and add your API keys.

### 4. Run

```bash
python main.py
```

## Files

- `main.py` - Main bot application
- `run_bot.py` - GitHub Actions script runner
- `test_setup.py` - Local API testing script
- `.github/workflows/tweet.yml` - Daily automated posting (12:15 AM UTC)
- `.github/workflows/test_a_tweet.yml` - Manual test workflow
- `posted_quotes.json` - Duplicate prevention storage
- `.env` - Your API credentials (create from .env.example)

## 🤖 GitHub Actions Automation

The bot can run automatically every day using GitHub Actions (FREE!).

### Setup Steps:

1. **Fork this repository** to your GitHub account

2. **Add GitHub Secrets** (Repository Settings → Secrets → Actions):
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   TWITTER_API_KEY=your_twitter_api_key_here
   TWITTER_API_SECRET=your_twitter_api_secret_here
   TWITTER_ACCESS_TOKEN=your_twitter_access_token_here
   TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret_here
   ```

3. **Enable GitHub Actions** in your repository (Actions tab)

4. **The workflow will**:
   - Run daily at 12:15 AM UTC (customize in `tweet.yml`)
   - Generate and post a motivational quote
   - Update `posted_quotes.json` to prevent duplicates
   - Show results in Actions tab

### Manual Trigger:
- **Daily Tweet**: Go to **Actions** tab → **Daily AI Motivational Tweet** → **Run workflow**
- **Test Tweet**: Go to **Actions** tab → **Test A Tweet** → **Run workflow**
  - Optional: Specify custom theme and max length
  - Perfect for testing before going live

### Customize Schedule:
Edit `.github/workflows/tweet.yml` cron schedule:
```yaml
# Daily at 12:15 AM UTC (current setting)
- cron: '15 0 * * *'

# Daily at 9 AM UTC
- cron: '0 9 * * *'

# Every 6 hours
- cron: '0 */6 * * *'

# Twice daily (9 AM and 9 PM UTC)
- cron: '0 9,21 * * *'
```

## 🛠️ Local Development

### Test Setup:
```bash
python test_setup.py
```

### Run Locally:
```bash
python main.py
```

### Manual Single Post:
```bash
python run_bot.py
```
