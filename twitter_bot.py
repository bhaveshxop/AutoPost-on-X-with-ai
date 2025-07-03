import tweepy
import logging
from typing import Optional

class TwitterBot:
    def __init__(self, api_key: str, api_secret: str, access_token: str, 
                 access_token_secret: str, bearer_token: str):
        """Initialize Twitter API client using X API v2 with OAuth 2.0 User Context"""
        try:
            # Use OAuth 2.0 User Context for posting tweets
            self.client = tweepy.Client(
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
                wait_on_rate_limit=True
            )
            
            # Test authentication by getting user info
            me = self.client.get_me()
            if me.data:
                self.user_id = me.data.id
                self.username = me.data.username
                logging.info(f"Twitter authentication successful for @{self.username}")
            else:
                raise Exception("Failed to get user info")
            
        except Exception as e:
            logging.error(f"Twitter authentication failed: {e}")
            raise
    
    def post_tweet(self, text: str) -> Optional[dict]:
        """Post a tweet using X API v2"""
        try:
            # Ensure tweet is within character limit
            if len(text) > 280:
                text = text[:277] + "..."
            
            # Post tweet using tweepy
            response = self.client.create_tweet(text=text)
            
            if response.data:
                tweet_id = response.data['id']
                
                logging.info(f"Tweet posted successfully! ID: {tweet_id}")
                logging.info(f"Tweet content: {text}")
                
                return {
                    'id': tweet_id,
                    'text': text,
                    'success': True
                }
            else:
                logging.error("Failed to post tweet - no data returned")
                return None
            
        except tweepy.TooManyRequests:
            logging.error("Rate limit exceeded. Please wait before posting again.")
            return None
            
        except tweepy.Forbidden as e:
            logging.error(f"Twitter API forbidden error: {e}")
            logging.error("Check your app permissions - it needs 'Read and Write' access")
            return None
            
        except Exception as e:
            logging.error(f"Error posting tweet: {e}")
            return None
    
    def get_account_info(self) -> Optional[dict]:
        """Get account information"""
        try:
            user = self.client.get_me(user_fields=['public_metrics'])
            
            if user.data:
                return {
                    'username': user.data.username,
                    'name': user.data.name,
                    'followers': user.data.public_metrics.get('followers_count', 0) if user.data.public_metrics else 0,
                    'following': user.data.public_metrics.get('following_count', 0) if user.data.public_metrics else 0
                }
            else:
                logging.error("Error getting account info: No data returned")
                return None
                
        except Exception as e:
            logging.error(f"Error getting account info: {e}")
            return None
    
    def get_recent_tweets(self, count: int = 10) -> list:
        """Get recent tweets to avoid duplicates"""
        try:
            # Limit count to API maximum
            count = min(count, 10)
            
            tweets = self.client.get_users_tweets(
                id=self.user_id,
                max_results=count,
                tweet_fields=['text']
            )
            
            if tweets.data:
                return [tweet.text for tweet in tweets.data]
            else:
                return []
                
        except Exception as e:
            logging.error(f"Error getting recent tweets: {e}")
            return []
    
    def is_duplicate(self, text: str, recent_tweets: list = None) -> bool:
        """Check if the tweet content is similar to recent tweets"""
        if not recent_tweets:
            recent_tweets = self.get_recent_tweets()
        
        # Simple duplicate detection - check if similar content exists
        text_lower = text.lower()
        for tweet in recent_tweets:
            tweet_lower = tweet.lower()
            # Check if 70% of words are the same
            text_words = set(text_lower.split())
            tweet_words = set(tweet_lower.split())
            if len(text_words) > 0:
                similarity = len(text_words.intersection(tweet_words)) / len(text_words)
                if similarity > 0.7:
                    return True
        return False
