import os
import logging
import time
import random
import schedule
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
import tweepy
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

class MotivationalBot:
    def __init__(self):
        """Initialize the AI motivational quote bot"""
        self.setup_apis()
        self.posted_quotes = self.load_posted_quotes()
        self.themes = [
            "coding", "debugging", "software engineering", "programming", 
            "tech career", "developer life", "algorithms", "problem solving",
            "clean code", "continuous learning", "tech innovation", "git workflow"
        ]
        
    def setup_apis(self):
        """Setup Gemini AI and Twitter API clients"""
        try:
            # Initialize Gemini AI
            gemini_key = os.getenv('GEMINI_API_KEY')
            if not gemini_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables")
            
            genai.configure(api_key=gemini_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            logging.info("Gemini AI initialized successfully")
            
            # Initialize Twitter API
            self.twitter_client = tweepy.Client(
                consumer_key=os.getenv('TWITTER_API_KEY'),
                consumer_secret=os.getenv('TWITTER_API_SECRET'),
                access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
                access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
                wait_on_rate_limit=True
            )
            
            # Test Twitter authentication
            me = self.twitter_client.get_me()
            if me.data:
                self.user_id = me.data.id
                self.username = me.data.username
                logging.info(f"Twitter authentication successful for @{self.username}")
            else:
                raise Exception("Failed to get Twitter user info")
            
        except Exception as e:
            logging.error(f"Error setting up APIs: {e}")
            raise
    
    def generate_quote(self, theme=None, max_length=260):
        """Generate a motivational quote using Gemini AI"""
        try:
            if not theme:
                theme = random.choice(self.themes)
            
            prompt = f"""Generate a powerful, original motivational quote about {theme} for software engineers and developers. 
            Requirements:
            - Maximum {max_length} characters
            - Inspiring and actionable for programmers
            - Original and unique
            - No quotation marks
            - No hashtags
            - Professional and positive tone
            - Relatable to coding, programming, or tech industry
            
            Example format: "Code is poetry written in logic. Debug your mind, optimize your life."
            
            Generate one quote about {theme} for software engineers:"""
            
            response = self.gemini_model.generate_content(prompt)
            quote = response.text.strip()
            
            # Clean up the quote
            quote = quote.replace('"', '').replace("'", "'")
            
            # Ensure it's within character limit
            if len(quote) > max_length:
                # Truncate quote at word boundary
                words = quote.split()
                truncated = ""
                for word in words:
                    if len(truncated + " " + word) <= max_length - 3:
                        truncated += " " + word if truncated else word
                    else:
                        break
                quote = truncated + "..."
            
            logging.info(f"Generated quote: {quote}")
            return quote
            
        except Exception as e:
            logging.error(f"Error generating quote: {e}")
            # Fallback tech quotes
            fallback_quotes = [
                "Code is poetry written in logic. Debug your mind, optimize your life.",
                "Every bug is a lesson in disguise. Keep coding, keep learning.",
                "Great software is built one commit at a time. Progress over perfection.",
                "In code we trust, in testing we verify. Ship with confidence.",
                "Refactor your code, refactor your thinking. Clean code, clear mind."
            ]
            return random.choice(fallback_quotes)
    
    def post_tweet(self, text):
        """Post a tweet to Twitter"""
        try:
            if len(text) > 280:
                text = text[:277] + "..."
            
            response = self.twitter_client.create_tweet(text=text)
            
            if response.data:
                tweet_id = response.data['id']
                logging.info(f"Tweet posted successfully! ID: {tweet_id}")
                logging.info(f"Tweet content: {text}")
                return {'id': tweet_id, 'text': text, 'success': True}
            else:
                logging.error("Failed to post tweet - no data returned")
                return None
                
        except Exception as e:
            logging.error(f"Error posting tweet: {e}")
            return None
    
    def is_duplicate(self, text):
        """Check if the quote is a duplicate"""
        return text in self.posted_quotes
    
    def load_posted_quotes(self):
        """Load previously posted quotes"""
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
            
            max_length = int(os.getenv('MAX_QUOTE_LENGTH', 260))
            themes = os.getenv('QUOTE_THEMES', 'motivation,success,inspiration').split(',')
            
            attempts = 0
            max_attempts = 5
            
            while attempts < max_attempts:
                theme = themes[attempts % len(themes)] if themes else None
                quote = self.generate_quote(theme, max_length)
                
                if not self.is_duplicate(quote):
                    result = self.post_tweet(quote)
                    
                    if result and result.get('success'):
                        self.posted_quotes.add(quote)
                        self.save_posted_quotes()
                        logging.info(f"Successfully posted quote: {quote}")
                        return result
                    else:
                        logging.error("Failed to post tweet")
                else:
                    logging.info(f"Quote is duplicate, generating new one... (attempt {attempts + 1})")
                
                attempts += 1
                time.sleep(2)
            
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
        
        schedule.every(interval_hours).hours.do(self.generate_and_post)
        
        logging.info(f"Bot scheduled to post every {interval_hours} hours")
        print(f"🤖 Bot started! Will post every {interval_hours} hours")
        print("⏰ Next post scheduled at:", 
              datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("Press Ctrl+C to stop")
        
        # Run immediately on start
        self.generate_and_post()
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            logging.info("Bot stopped by user")
            print("\n🛑 Bot stopped")

def main():
    """Main function"""
    print("🚀 AI Motivational Quote Bot")
    print("=" * 40)
    
    try:
        bot = MotivationalBot()
        
        print(f"📱 Connected to Twitter: @{bot.username}")
        
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
