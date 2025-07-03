import os
import logging
import time
import schedule
from datetime import datetime
from dotenv import load_dotenv
from gemini_quote_generator import GeminiQuoteGenerator
from twitter_bot import TwitterBot
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

class MotivationalBot:
    def __init__(self):
        """Initialize the motivational bot"""
        self.setup_apis()
        self.posted_quotes = self.load_posted_quotes()
        
    def setup_apis(self):
        """Setup API clients"""
        try:
            # Initialize Gemini API
            gemini_key = os.getenv('GEMINI_API_KEY')
            if not gemini_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables")
            
            self.quote_generator = GeminiQuoteGenerator(gemini_key)
            logging.info("Gemini API initialized successfully")
            
            # Initialize Twitter API
            twitter_credentials = {
                'api_key': os.getenv('TWITTER_API_KEY'),
                'api_secret': os.getenv('TWITTER_API_SECRET'),
                'access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
                'access_token_secret': os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
                'bearer_token': os.getenv('TWITTER_BEARER_TOKEN')
            }
            
            missing_creds = [k for k, v in twitter_credentials.items() if not v]
            if missing_creds:
                raise ValueError(f"Missing Twitter credentials: {missing_creds}")
            
            self.twitter_bot = TwitterBot(**twitter_credentials)
            logging.info("Twitter API initialized successfully")
            
        except Exception as e:
            logging.error(f"Error setting up APIs: {e}")
            raise
    
    def load_posted_quotes(self) -> set:
        """Load previously posted quotes to avoid duplicates"""
        try:
            with open('posted_quotes.json', 'r') as f:
                return set(json.load(f))
        except FileNotFoundError:
            return set()
    
    def save_posted_quotes(self):
        """Save posted quotes to file"""
        try:
            with open('posted_quotes.json', 'w') as f:
                json.dump(list(self.posted_quotes), f, indent=2)
        except Exception as e:
            logging.error(f"Error saving posted quotes: {e}")
    
    def generate_and_post(self):
        """Generate a quote and post to Twitter"""
        try:
            logging.info("Starting quote generation and posting process...")
            
            # Get configuration
            max_length = int(os.getenv('MAX_QUOTE_LENGTH', 260))
            themes = os.getenv('QUOTE_THEMES', 'motivation,success,inspiration').split(',')
            
            # Generate multiple quotes and pick the best one
            attempts = 0
            max_attempts = 5
            
            while attempts < max_attempts:
                # Generate quote
                theme = themes[attempts % len(themes)] if themes else None
                quote = self.quote_generator.generate_quote(theme, max_length)
                
                # Check for duplicates
                if quote not in self.posted_quotes and not self.twitter_bot.is_duplicate(quote):
                    # Post to Twitter
                    result = self.twitter_bot.post_tweet(quote)
                    
                    if result and result.get('success'):
                        # Save to posted quotes
                        self.posted_quotes.add(quote)
                        self.save_posted_quotes()
                        
                        logging.info(f"Successfully posted quote: {quote}")
                        return result
                    else:
                        logging.error("Failed to post tweet")
                        
                else:
                    logging.info(f"Quote is duplicate, generating new one... (attempt {attempts + 1})")
                
                attempts += 1
                time.sleep(2)  # Brief delay between attempts
            
            logging.error("Failed to generate unique quote after maximum attempts")
            return None
            
        except Exception as e:
            logging.error(f"Error in generate_and_post: {e}")
            return None
    
    def run_once(self):
        """Run the bot once"""
        logging.info("Running motivational bot...")
        result = self.generate_and_post()
        
        if result:
            print(f"✅ Quote posted successfully!")
            print(f"📝 Content: {result['text']}")
            print(f"🔗 Tweet ID: {result['id']}")
        else:
            print("❌ Failed to post quote")
    
    def run_scheduled(self):
        """Run the bot on a schedule"""
        interval_hours = int(os.getenv('POST_INTERVAL_HOURS', 6))
        
        # Schedule the job
        schedule.every(interval_hours).hours.do(self.generate_and_post)
        
        logging.info(f"Bot scheduled to post every {interval_hours} hours")
        print(f"🤖 Bot started! Will post every {interval_hours} hours")
        print("⏰ Next post scheduled at:", 
              datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("Press Ctrl+C to stop")
        
        # Run immediately on start
        self.generate_and_post()
        
        # Keep the script running
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logging.info("Bot stopped by user")
            print("\n🛑 Bot stopped")

def main():
    """Main function"""
    print("🚀 AI Motivational Quote Bot")
    print("=" * 40)
    
    try:
        bot = MotivationalBot()
        
        # Get account info
        account_info = bot.twitter_bot.get_account_info()
        if account_info:
            print(f"📱 Connected to Twitter: @{account_info['username']}")
            print(f"👥 Followers: {account_info['followers']}")
        
        # Ask user for run mode
        print("\nChoose run mode:")
        print("1. Run once (post single quote)")
        print("2. Run on schedule (continuous posting)")
        
        choice = input("\nEnter choice (1 or 2): ").strip()
        
        if choice == "1":
            bot.run_once()
        elif choice == "2":
            bot.run_scheduled()
        else:
            print("Invalid choice. Running once...")
            bot.run_once()
            
    except Exception as e:
        logging.error(f"Bot startup failed: {e}")
        print(f"❌ Error: {e}")
        print("\n💡 Make sure you have:")
        print("   1. Created .env file with API keys")
        print("   2. Installed requirements: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
