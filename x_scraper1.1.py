import tweepy
import pandas as pd
import json
from datetime import datetime

class TwitterScraper:
    
    def __init__(self, bearer_token):
        self.client = tweepy.Client(bearer_token=bearer_token)
        self.tweets_data = []
        self.seen_tweet_ids = set()
    
    def scrape_by_username(self, username, max_tweets=100, start_time=None):
        print(f"Scraping from @{username}...")
        
        try:
            user = self.client.get_user(username=username)
            if not user.data:
                print(f"User @{username} not found")
                return []
            
            user_id = user.data.id
            
            kwargs = {
                'id': user_id,
                'max_results': min(max_tweets, 100),
                'tweet_fields': ['created_at', 'public_metrics', 'text']
            }
            
            if start_time:
                if isinstance(start_time, str):
                    start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                kwargs['start_time'] = start_time
            
            tweets = self.client.get_users_tweets(**kwargs)
            
            if tweets.data:
                for tweet in tweets.data:
                    if tweet.id not in self.seen_tweet_ids:
                        self.tweets_data.append({
                            'date': tweet.created_at,
                            'username': username,
                            'tweet_id': tweet.id,
                            'content': tweet.text,
                            'url': f"https://twitter.com/{username}/status/{tweet.id}"
                        })
                        self.seen_tweet_ids.add(tweet.id)
            
            print(f"Scraped {len(self.tweets_data)} total tweets (skipped duplicates)")
            return self.tweets_data
            
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def save_to_csv(self, filename='[ ].csv'): # change the saved .csv file name here
        if not self.tweets_data:
            print("No data")
            return
        
        df = pd.DataFrame(self.tweets_data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    
    def save_to_json(self, filename='tweets.json'):
        if not self.tweets_data:
            print("No data")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.tweets_data, f, ensure_ascii=False, indent=4, default=str)
        print(f"Data saved to {filename}")
    
    def get_dataframe(self):
        if not self.tweets_data:
            print("No data")
            return None
        
        return pd.DataFrame(self.tweets_data)
    
    def clear_data(self):
        self.tweets_data = []
        self.seen_tweet_ids = set()
        print("Data cleared")
