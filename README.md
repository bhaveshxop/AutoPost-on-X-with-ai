# AutoPost on X using Gemini AI and GitHub Actions

🤖 **Automated Twitter Bot** that generates and posts AI-powered motivational quotes for developers daily using Google Gemini AI and GitHub Actions automation.

## ✨ Features

- 🤖 **AI-Generated Content** - Powered by Google Gemini AI (FREE)
- 🐦 **Auto-Post to X/Twitter** - Fully automated posting (FREE - 1,500 tweets/month)
- ⏰ **GitHub Actions Automation** - Runs daily at 1:00 AM UTC
- 🔄 **Duplicate Prevention** - Smart tracking to avoid repeat quotes
- 🎯 **Developer-Focused** - Motivational quotes tailored for programmers
- 🚀 **Zero Maintenance** - Set it and forget it automation

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

## 📁 Files

- `main.py` - Main bot application with AI quote generation
- `run_bot.py` - GitHub Actions script runner
- `.github/workflows/tweet.yml` - Daily automated posting (1:00 AM UTC)
- `posted_quotes.json` - Duplicate prevention storage
- `.env` - Your API credentials (create from .env.example)
- `requirements.txt` - Python dependencies

## 🤖 GitHub Actions Automation (Recommended)

**Fully automated daily tweets using GitHub Actions - completely FREE!**

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

4. **The workflow will automatically**:
   - Run daily at **1:00 AM UTC** (customize in `tweet.yml`)
   - Generate AI-powered motivational quotes using Gemini
   - Post to your X/Twitter account
   - Update `posted_quotes.json` to prevent duplicates
   - Show results in Actions tab

### Manual Trigger (Optional):

- Go to **Actions** tab → **"Daily AI Motivational Tweet"** → **"Run workflow"**
- Perfect for testing or posting extra tweets

### Customize Schedule:

Edit `.github/workflows/tweet.yml` cron schedule:

```yaml
# Daily at 1:00 AM UTC (current setting)
- cron: "0 1 * * *"
# Daily at 9 AM UTC
- cron: "0 9 * * *"

# Every 6 hours
- cron: "0 */6 * * *"

# Twice daily (9 AM and 9 PM UTC)
- cron: "0 9,21 * * *"
```

## 🛠️ Local Development (Optional)

### Run Locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run interactive mode
python main.py

# Run single post
python run_bot.py
```

## 🚀 Getting Started

1. **Fork this repository**
2. **Get your FREE API keys** (links in setup section)
3. **Add GitHub Secrets** with your API keys
4. **Watch the magic happen** - daily automated tweets!

## 📱 Sample Tweet Themes

Your bot will generate quotes about:

- 💻 Coding & Programming
- 🐛 Debugging & Problem Solving
- 🏗️ Software Engineering
- 📈 Tech Career Growth
- 🔧 Clean Code & Best Practices
- 📚 Continuous Learning

---

**🎯 Perfect for developers who want to maintain an active, inspiring Twitter presence without the daily effort!**
