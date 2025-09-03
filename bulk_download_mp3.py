import csv
import os
import yt_dlp

def read_urls_from_csv(csv_filename):
    urls = []
    with open(csv_filename, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        for row in reader:
            if row and row[0].startswith("http"):
                urls.append(row[0])
    return urls

#downloaded .mp3 files will be automatically placed in the "downloads" folder inside the scraper folder
    #"downloads" will be created automatically when running this file for the first time
def bulk_download(urls, output_dir="downloads"):        #change output folder name here
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'ignoreerrors': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s [%(id)s].%(ext)s'),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)

if __name__ == "__main__":
    #build dateframe
    csv_filename = "rumble_videos.csv"
    urls = read_urls_from_csv(csv_filename)
    print(f"Found {len(urls)} URLs to download as MP3")
    bulk_download(urls)
