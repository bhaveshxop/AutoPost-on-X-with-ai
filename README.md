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
- `gemini_quote_generator.py` - AI quote generation
- `twitter_bot.py` - Twitter posting
- `.env` - Your API credentials (create from .env.example)
