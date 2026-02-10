"""
File: format_codex_jsonl.py
Project: Zombie Waves AI Codex
Author: Andrew
Date: 2026-02-09
Description: Converts detoxed clean-discord JSON output into a structured JSONL 
             dataset for Llama 3 fine-tuning, anonymizing usernames and 
             filtering for high-signal content.
"""

import json
import re
import os

# Configuration
INPUT_FILE = r"C:\inetpub\wwwroot\GitHub\clean-discord\data\cleaned\[1191318864139649124].json" 
OUTPUT_FILE = "./data/zombie_waves_dataset.jsonl"
SYSTEM_PROMPT = "You are the Zombie Waves AI Codex, an expert strategy assistant."

def clean_message(text):
    """Strips 'Username: ' from the start of the message strings."""
    return re.sub(r"^[A-Za-z0-9_\-\.]{2,32}(#\d{4})?:\s?", "", text).strip()

def create_jsonl():
    # Helper to check if the file actually exists before we start
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: Could not find the file at:\n{INPUT_FILE}")
        print("Please ensure the filename at the end of the path is correct!")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    conversations = data.get("conversations", [])
    count = 0

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        for convo in conversations:
            for msg_pair in convo:
                # msg_pair[0] is the text content from your JSON snippet
                raw_text = msg_pair[0]
                clean_text = clean_message(raw_text)
                
                if len(clean_text) > 25:
                    entry = {
                        "instruction": "Provide a tip or strategy for Zombie Waves.",
                        "input": "",
                        "output": clean_text,
                        "system": SYSTEM_PROMPT
                    }
                    outfile.write(json.dumps(entry) + "\n")
                    count += 1

    print(f"✅ Success! Processed {count} entries into {OUTPUT_FILE}")

if __name__ == "__main__":
    create_jsonl()