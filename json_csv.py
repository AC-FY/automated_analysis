import json
import os
import glob
import csv

# Configuration - modify these paths
JSON_FILES_PATH = "/Users/AndyCheng/Documents/202508transcripts"   # folder with your .json files
CSV_EXPORT_PATH = "/Users/AndyCheng/Documents/202508csv"  # where CSVs will be saved

def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def process_json_file(json_file_path):
    """Process one transcript JSON into grouped speaker segments and save to CSV"""
    print(f"Processing: {json_file_path}")
    
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if "results" not in data or "items" not in data["results"]:
        print(f"No transcription items in {json_file_path}")
        return False
    
    items = data["results"]["items"]
    rows = []
    current_speaker = None
    current_text = []
    start_time = None
    end_time = None
    
    for item in items:
        if item["type"] == "pronunciation":
            word = item["alternatives"][0]["content"]
            speaker = item.get("speaker_label", "unknown")
            
            if current_speaker is None:
                current_speaker = speaker
                start_time = float(item["start_time"])
            
            if speaker != current_speaker:
                # flush the old speaker’s segment
                rows.append({
                    "speaker": current_speaker,
                    "start_time": format_timestamp(start_time),
                    "end_time": format_timestamp(end_time),
                    "text": " ".join(current_text)
                })
                # reset for new speaker
                current_speaker = speaker
                start_time = float(item["start_time"])
                current_text = []
            
            current_text.append(word)
            end_time = float(item["end_time"])
        
        elif item["type"] == "punctuation":
            # add punctuation to last word
            if current_text:
                current_text[-1] = current_text[-1] + item["alternatives"][0]["content"]
    
    # flush last segment
    if current_text:
        rows.append({
            "speaker": current_speaker,
            "start_time": format_timestamp(start_time),
            "end_time": format_timestamp(end_time),
            "text": " ".join(current_text)
        })
    
    if not rows:
        print(f"No segments extracted from {json_file_path}")
        return False
    
    # Export to CSV
    os.makedirs(CSV_EXPORT_PATH, exist_ok=True)
    csv_file_path = os.path.join(
        CSV_EXPORT_PATH, os.path.basename(json_file_path).replace(".json", ".csv")
    )
    with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["speaker", "start_time", "end_time", "text"])
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Saved CSV: {csv_file_path}")
    return True

def main():
    json_files = glob.glob(os.path.join(JSON_FILES_PATH, "*.json"))
    if not json_files:
        print("No JSON files found in input folder.")
        return
    for jf in json_files:
        process_json_file(jf)

if __name__ == "__main__":
    main()
