This is a repo for CPOST APV automated analysis codes.

Currently, the automated analysis pipeline is dependent on three separate processes: data scraping, data merging ,and topic classification.

Data scraping is consisted of sub-processes: Rumble scraping and Telegram scraping.

Rumble scraping is performed by rumble_scraper_v3.py and bulk_download_mp3.py.
Telegram scraping is performed by the weekly-run legacy Telegram scraper codes from Will Fitz.

Data merging is 

BERT_LDA.py is for document classification, and BERT_LDA_v2.py is for sentence-by-sentence classification.
