"""
Filename: youtube_to_chatml.py
Project: Zombie Waves AI Codex
Description:
    Processes the project's strategy playlist. It synthesises 'User-Question' 
    and 'Assistant-Response' pairs in ChatML format.
"""

import os
import json
import sys
from pytubefix import Playlist
from youtube_transcript_api import YouTubeTranscriptApi
import time
import random

# --- CONFIGURATION ---
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLWnpSHoOSdjMA-8DC7nujEedmgDjwrnGK"
OUTPUT_FILE = "./data/zombie_waves_youtube_chatml.jsonl"
MAX_CHAR_LENGTH = 3500  # Stays well within the 1024 token limit for 4GB rigs

SYSTEM_PROMPT = (
    "You are the Zombie Waves AI Codex, an expert strategy assistant. "
    "Your goal is to provide accurate, concise, and helpful gameplay advice "
    "for Zombie Waves. Stay in character and only discuss Zombie Waves content."
)

def clean_text(text):
    """Simple sanitisation of common YouTube transcript noise."""
    unwanted = ["[Music]", "[Laughter]", "subscribe", "hit the bell", "hey guys"]
    for phrase in unwanted:
        text = text.replace(phrase, "")
    return " ".join(text.split())

def process_playlist():
    print(f"🚀 Initialising playlist extraction...")
    try:
        pl = Playlist(PLAYLIST_URL)
        print(f"📂 Found {len(pl.videos)} videos in playlist: {pl.title}")
    except Exception as e:
        print(f"❌ Failed to load playlist: {e}")
        return

    count = 0
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for video in pl.videos:
            v_id = video.video_id
            title = video.title
            
            print(f"🔍 Processing: {title} ({v_id})")
            
            try:
                # Fetch transcript
                # 1. Use .fetch() instead of .get_transcript()
                # This handles auto-generated subtitles by default
                ytt_api = YouTubeTranscriptApi()
                fetched_transcript = ytt_api.fetch(v_id, languages=['en'])
                
                # 2. Extract the text from the new object structure
                raw_text = " ".join([entry.text for entry in fetched_transcript])
                
                cleaned_content = clean_text(raw_text)

                # Cap content to ensure 4GB VRAM safety (Max 1024 tokens approx)
                if len(cleaned_content) > MAX_CHAR_LENGTH:
                    cleaned_content = cleaned_content[:MAX_CHAR_LENGTH] + "..."

                # Construct ChatML Entry
                chat_entry = {
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"Based on the guide '{title}', what are the key strategies?"},
                        {"role": "assistant", "content": cleaned_content}
                    ]
                }
                
                f.write(json.dumps(chat_entry) + "\n")
                count += 1

                # After processing a video, wait before the next one
                wait_time = random.uniform(5, 12)  # Wait 5 to 12 seconds
                print(f"⏳ Sleeping for {wait_time:.1f}s to avoid IP throttle...")
                time.sleep(wait_time)
                
            except Exception as e:
                print(f"⚠️ Skipping {v_id} (Transcript likely disabled): {e}")

    print(f"\n✅ Success! Generated {count} ChatML entries in {OUTPUT_FILE}")

if __name__ == "__main__":
    # Standard check: Ensure we aren't accidentally running as root
    if os.geteuid() == 0:
        print("🛑 Security Alert: Do not run this script as root. Use your 'codex' profile.")
        sys.exit(1)
        
    process_playlist()