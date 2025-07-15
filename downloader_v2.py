#!/usr/bin/env python3
import argparse
import csv
import os
import platform
import shutil
import sys

import yt_dlp

def check_ffmpeg():
    """Check for ffmpeg and ffprobe. Return True if both found."""
    has_ffmpeg = shutil.which("ffmpeg") is not None
    has_ffprobe = shutil.which("ffprobe") is not None
    if not (has_ffmpeg and has_ffprobe):
        print("\nWarning: ffmpeg and/or ffprobe not found. Audio will be downloaded in original format without MP3 conversion.\n")
    return has_ffmpeg and has_ffprobe


def read_urls_from_csv(csv_filename):
    """Read video URLs from the first column of a CSV (skipping header)."""
    urls = []
    try:
        with open(csv_filename, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row and row[0].startswith(("http://", "https://")):
                    urls.append(row[0])
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_filename}' not found.")
        sys.exit(1)
    return urls


def bulk_download(urls, output_dir, use_ffmpeg):
    """Download audio from URLs, converting to MP3 if ffmpeg is available."""
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'ignoreerrors': True,
        'outtmpl': os.path.join(output_dir, '%(title)s [%(id)s].%(ext)s'),
    }
    if use_ffmpeg:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)


def main():
    parser = argparse.ArgumentParser(
        description="Download audio from URLs in a CSV; convert to MP3 if possible."
    )
    parser.add_argument(
        "--csv", "-c",
        default="rumble_videos.csv",
        help="Path to CSV file (URLs in first column). Defaults to 'rumble_videos.csv'."
    )
    parser.add_argument(
        "--outdir", "-o",
        default="downloads",
        help="Directory to save downloaded files."
    )
    args = parser.parse_args()

    ffmpeg_available = check_ffmpeg()
    urls = read_urls_from_csv(args.csv)
    if not urls:
        print(f"No valid URLs found in '{args.csv}'.")
        sys.exit(1)

    print(f"Found {len(urls)} URL(s) in '{args.csv}'. Starting download...")
    bulk_download(urls, args.outdir, ffmpeg_available)
    print(f"\nDownloads complete. Files are in: {os.path.abspath(args.outdir)}")

if __name__ == "__main__":
    main()
