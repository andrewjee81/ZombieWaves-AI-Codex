"""
File: convert_reddit_to_chatml.py
Project: Zombie Waves AI Codex
Author: Andrew
Description: Converts Alpaca-style Reddit JSONL into conversational ChatML.
"""

import json
import os
import sys
from pathlib import Path

# Adjust path to import from your project root
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from config import LOCAL_DATA_DIR, SYSTEM_PROMPT

# PATH CONFIGURATION
# Using r"" for Windows path safety
INPUT_FILE = os.path.join(LOCAL_DATA_DIR, "reddit_paired_data.jsonl")
OUTPUT_FILE = os.path.join(LOCAL_DATA_DIR, "zombie_waves_reddit_chatml.jsonl")

# The "Guardrail" System Prompt loaded from config

def convert_reddit():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: {INPUT_FILE} not found!")
        return

    count = 0
    with open(INPUT_FILE, 'r', encoding='utf-8') as f_in, \
         open(OUTPUT_FILE, 'w', encoding='utf-8') as f_out:
        
        for line in f_in:
            line = line.strip()
            if not line: continue
            
            try:
                data = json.loads(line)
                
                # MAPPING: "instruction" -> User, "response" -> Assistant
                user_q = data.get("instruction")
                assistant_a = data.get("response")
                
                if user_q and assistant_a:
                    chat_entry = {
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": str(user_q).strip()},
                            {"role": "assistant", "content": str(assistant_a).strip()}
                        ]
                    }
                    f_out.write(json.dumps(chat_entry) + "\n")
                    count += 1
            except json.JSONDecodeError:
                continue
                
    print(f"✅ Successfully converted {count} Reddit tips into ChatML format.")

if __name__ == "__main__":
    convert_reddit()