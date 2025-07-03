import os
import tweepy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_twitter_auth():
    """Test Twitter authentication step by step"""
    print("🧪 Testing Twitter Authentication...")
    print("=" * 50)
    
    # Get credentials
    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    client_id = os.getenv('TWITTER_CLIENT_ID')
    client_secret = os.getenv('TWITTER_CLIENT_SECRET')
    
    print(f"✅ API Key: {api_key[:10]}..." if api_key else "❌ API Key missing")
    print(f"✅ API Secret: {api_secret[:10]}..." if api_secret else "❌ API Secret missing")
    print(f"✅ Access Token: {access_token[:10]}..." if access_token else "❌ Access Token missing")
    print(f"✅ Access Token Secret: {access_token_secret[:10]}..." if access_token_secret else "❌ Access Token Secret missing")
    print(f"✅ Bearer Token: {bearer_token[:10]}..." if bearer_token else "❌ Bearer Token missing")
    print(f"✅ Client ID: {client_id[:10]}..." if client_id else "❌ Client ID missing")
    print(f"✅ Client Secret: {client_secret[:10]}..." if client_secret else "❌ Client Secret missing")
    
    print("\n🔗 Testing OAuth 1.0a Authentication...")
    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            wait_on_rate_limit=True
        )
        
        me = client.get_me()
        if me.data:
            print(f"✅ OAuth 1.0a Success: @{me.data.username}")
            return True
        else:
            print("❌ OAuth 1.0a Failed: No user data returned")
            return False
            
    except Exception as e:
        print(f"❌ OAuth 1.0a Failed: {e}")
        return False

def test_bearer_token():
    """Test Bearer Token authentication"""
    print("\n🔗 Testing Bearer Token Authentication...")
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    
    try:
        client = tweepy.Client(bearer_token=bearer_token)
        
        # Test with a simple public API call
        tweets = client.search_recent_tweets(query="hello", max_results=10)
        if tweets.data:
            print(f"✅ Bearer Token Success: Found {len(tweets.data)} tweets")
            return True
        else:
            print("❌ Bearer Token Failed: No data returned")
            return False
            
    except Exception as e:
        print(f"❌ Bearer Token Failed: {e}")
        return False

if __name__ == "__main__":
    oauth_success = test_twitter_auth()
    bearer_success = test_bearer_token()
    
    print("\n" + "=" * 50)
    if oauth_success:
        print("🎉 OAuth 1.0a authentication working!")
        print("   The bot should be able to post tweets.")
    else:
        print("❌ OAuth 1.0a authentication failed.")
        print("   Please check your Access Token and Access Token Secret.")
        print("   Make sure you regenerated them after changing app permissions.")
    
    if bearer_success:
        print("✅ Bearer Token working for read operations.")
    else:
        print("⚠️  Bearer Token not working properly.")
    
    print("\n💡 Next steps:")
    if not oauth_success:
        print("   1. Go to Twitter Developer Portal")
        print("   2. Check app permissions are 'Read and Write'")
        print("   3. Regenerate Access Token and Access Token Secret")
        print("   4. Update your .env file with new tokens")
    else:
        print("   Your authentication is working! Try running the main bot again.")
