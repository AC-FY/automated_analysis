import tweepy
import pandas as pd
import json
from datetime import datetime

class TwitterScraper:
    
    def __init__(self, bearer_token):
        self.client = tweepy.Client(bearer_token=bearer_token)
        self.tweets_data = []
    
    def scrape_by_username(self, username, max_tweets=10):
        print(f"Scraping tweets from @{username}...")
        self.tweets_data = []
        
        try:
            user = self.client.get_user(username=username)
            if not user.data:
                print(f"User @{username} not found")
                return []
            
            user_id = user.data.id
            
            tweets = self.client.get_users_tweets(
                id=user_id,
                max_results=min(max_tweets, 10),
                tweet_fields=['created_at', 'public_metrics', 'text']
            )
            
            if tweets.data:
                for tweet in tweets.data:
                    self.tweets_data.append({
                        'date': tweet.created_at,
                        'username': username,
                        'tweet_id': tweet.id,
                        'content': tweet.text,
                        'reply_count': tweet.public_metrics['reply_count'],
                        'retweet_count': tweet.public_metrics['retweet_count'],
                        'like_count': tweet.public_metrics['like_count'],
                        'url': f"https://twitter.com/{username}/status/{tweet.id}"
                    })
            
            print(f"Scraped {len(self.tweets_data)} tweets from @{username}")
            return self.tweets_data
            
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def save_to_csv(self, filename='tweets.csv'):
        if not self.tweets_data:
            print("No data to save. Please scrape tweets first.")
            return
        
        df = pd.DataFrame(self.tweets_data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    
    def save_to_json(self, filename='tweets.json'): # change json output name
        if not self.tweets_data:
            print("No data to save. Please scrape tweets first.")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.tweets_data, f, ensure_ascii=False, indent=4, default=str)
        print(f"Data saved to {filename}")
    
    def get_dataframe(self):
        if not self.tweets_data:
            print("No data available. Please scrape tweets first.")
            return None
        
        return pd.DataFrame(self.tweets_data)
