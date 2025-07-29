import requests
from bs4 import BeautifulSoup
import re
import os
import yt_dlp
import csv
from datetime import datetime

default_headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}

def get_rumble_video_urls(channel_url, max_pages=10):
    video_urls = []
    base_url = channel_url.rstrip('/')
    next_url = base_url

    for page in range(max_pages):
        print(f"Scraping page {page + 1}: {next_url}")
        try:
            resp = requests.get(next_url, headers=default_headers, timeout=20)
            resp.raise_for_status()
        except Exception as e:
            print(f"Request failed: {e}")
            break

        if not resp.ok:
            print(f"Failed to fetch {next_url} (HTTP {resp.status_code})")
            break

        soup = BeautifulSoup(resp.text, 'html.parser')

        for a in soup.find_all("a", href=True):
            href = a['href']
            if re.match(r"^/v[\w\-]+", href):
                full_url = "https://rumble.com" + href
                if full_url not in video_urls:
                    video_urls.append(full_url)

        load_more = soup.find("a", string=re.compile(r"Load More", re.I))
        if load_more and load_more.has_attr('href'):
            next_url = "https://rumble.com" + load_more['href']
        else:
            break

    print(f"Found {len(video_urls)} videos.")
    return video_urls

def get_video_metadata(video_url):
    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True}) as ydl:
            info = ydl.extract_info(video_url, download=False)
            raw_date = info.get('upload_date', '')
            if len(raw_date) == 8:
                date = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:]}"
            else:
                date = ''
            views = str(info.get('view_count', ''))
            return date, views
    except Exception as e:
        print(f"yt-dlp extraction failed: {e}")
        try:
            resp = requests.get(video_url, headers=default_headers, timeout=20)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            
            date_tag = soup.find('time')
            date = date_tag.get('datetime', '').split('T')[0] if date_tag else ''
            
            view_text = soup.find(text=re.compile(r"[0-9,]+ views", re.I))
            if view_text:
                m = re.search(r"([0-9,]+)", view_text)
                views = m.group(1).replace(',', '') if m else ''
            else:
                views = ''
                
            return date, views
        except Exception as e:
            print(f"Fallback extraction failed: {e}")
            return '', ''

def ensure_csv(csv_filename):
    if not os.path.exists(csv_filename):
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Video URL", "Date", "Viewer Count"])

def read_existing_urls(csv_filename):
    urls = set()
    if os.path.exists(csv_filename):
        with open(csv_filename, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None) 
            for row in reader:
                if row:
                    urls.add(row[0])
    return urls

def append_urls_to_csv(csv_filename, new_urls):
    ensure_csv(csv_filename) 
    
    with open(csv_filename, mode="a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for url in new_urls:
            date, views = get_video_metadata(url)
            writer.writerow([url, date, views])

if __name__ == "__main__":
    channel_url = "https://rumble.com/user/TheWarBoys?e9s=src_v1_cmd"
    video_urls = get_rumble_video_urls(channel_url, max_pages=2)

    csv_filename = "rumble_videos.csv"
    existing_urls = read_existing_urls(csv_filename)
    new_unique_urls = [url for url in video_urls if url not in existing_urls]

    if new_unique_urls:
        print(f"Found {len(new_unique_urls)} new videos. Adding to {csv_filename}")
        append_urls_to_csv(csv_filename, new_unique_urls)
        print(f"Added {len(new_unique_urls)} new URLs to {csv_filename}")
    else:
        print("No new URLs to add.")