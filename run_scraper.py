from x_scraper1_1 import TwitterScraper
BEARER_TOKEN = "YOUR_BEARER_TOKEN_HERE" # remember to use your own bearer token
	# bearer token 1 ## 
	# bearer token 2 ## 
scraper = TwitterScraper(BEARER_TOKEN)
scraper.scrape_by_username("elonmusk", max_tweets=100, start_time="2026-01-20T00:00:00Z") # change start_time here
scraper.save_to_csv("scraped_tweets.csv") # change the saved .csv file name here
