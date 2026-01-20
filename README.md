This is a repo for CPOST APV automated analysis codes.

Currently, the automated analysis pipeline is dependent on three separate processes: data scraping, merging, parsing, and topic classification.

Data scraping is consisted of sub-processes: Rumble scraping and Telegram scraping.

Rumble scraping is performed by rumble_scraper_v3.py and bulk_download_mp3.py.

Telegram scraping is performed by the weekly-run legacy Telegram scraper codes from Will Fitz.

Data merging is performed by json_csv.py.

BERT_LDA.py is for document classification, and BERT_LDA_v2.py is for sentence-by-sentence classification.

You are also very welcome to check out these two handbooks (WIP) for detailed instructions:
https://uchicagoedu-my.sharepoint.com/:w:/g/personal/andycfy_uchicago_edu1/IQAhfv4Z9zY_RonoaVxzLO1MAaoTgJblfSqQvp9Jgobplcw?e=Fma08E
and
https://uchicagoedu-my.sharepoint.com/:w:/g/personal/andycfy_uchicago_edu1/IQAHbnXXLcP6TI_Kxr6HMHcXAUo-5G5vy_xKRoLvi8HETf4?e=D404iW
