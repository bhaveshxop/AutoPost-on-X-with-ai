#!/usr/bin/env python3
"""
Simple script to run the motivational bot once for GitHub Actions
"""

import sys
import logging
from main import MotivationalBot

def main():
    """Run the bot once and exit with appropriate status code"""
    
    # Configure logging for GitHub Actions
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    
    try:
        print("🚀 Starting AI Motivational Tweet Bot...")
        
        # Initialize and run the bot
        bot = MotivationalBot()
        print(f"📱 Connected to Twitter: @{bot.username}")
        
        # Generate and post a quote
        result = bot.generate_and_post()
        
        if result and result.get('success'):
            print(f"✅ Successfully posted tweet!")
            print(f"📝 Content: {result['text']}")
            print(f"🔗 Tweet ID: {result['id']}")
            print(f"📊 Total quotes posted: {len(bot.posted_quotes)}")
            sys.exit(0)
        else:
            print("❌ Failed to post tweet")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        logging.error(f"Bot execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
