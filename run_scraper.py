from x_scraper import TwitterScraper
BEARER_TOKEN = "enter bearer token here"
	# bearer token 1 ## AAAAAAAAAAAAAAAAAAAAAJNK4gEAAAAA5GRNQU3EqL15JtTzcwOJf9hMIM4%3DinRS3tLGz2fJIo0T8GDXAqTJcEHcbOLP88rpH94Jf3b70GvyCh
	# bearer token 2 ## AAAAAAAAAAAAAAAAAAAAAGzn4gEAAAAAHUG7LIA%2FH9%2FmTPtf3ciwycfTeUc%3DXnCeyKuGAoSgZnusheP4WkQHzO5UBwv16QNJl82J52QpDTLY44
scraper = TwitterScraper(BEARER_TOKEN)
scraper.scrape_by_username("DHSgov", max_tweets=80, start_time="2025-01-20T00:00:00Z")
scraper.save_to_csv("dhs_tweets.csv")
