"""
File: discord_to_chatml.py
Project: Zombie Waves AI Codex
Author: Andrew
Description: Final conversion of detoxed Discord JSON into ChatML JSONL.
             Implements guardrails via a strict System Prompt.
"""

import json
import re
import os

# CONFIGURATION
INPUT_FILE = r"C:\inetpub\wwwroot\GitHub\clean-discord\data\cleaned\[1191318864139649124].json"
OUTPUT_FILE = "./data/zombie_waves_discord_chatml.jsonl"

# The "Guardrail" System Prompt
SYSTEM_PROMPT = (
    "You are the Zombie Waves AI Codex, an expert strategy assistant. "
    "Your goal is to provide accurate, concise, and helpful gameplay advice "
    "for Zombie Waves. Stay in character and only discuss Zombie Waves content."
)

def clean_username(text):
    """Strips the 'Username: ' header from the message content."""
    # Matches common Discord names like 'skyrim6291:' or 'User#1234:'
    return re.sub(r"^[A-Za-z0-9_\-\.]{2,32}(#\d{4})?:\s?", "", text).strip()

def transform_to_chatml():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: File not found at {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    conversations = data.get("conversations", [])
    formatted_count = 0

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        for convo in conversations:
            # We need at least 2 messages for a 'conversation' (Q&A)
            if len(convo) < 2:
                continue
            
            # Message 0 = The 'User' (Question/Prompt)
            user_msg = clean_username(convo[0][0])
            
            # Message 1+ = The 'Assistant' (Expert Advice)
            # We join them into one block if multiple people replied
            assistant_msg = " ".join([clean_username(m[0]) for m in convo[1:]])

            # Signal Filtering: Skip 'thank yous' or 'hellos'
            if len(user_msg) > 15 and len(assistant_msg) > 25:
                chat_entry = {
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_msg},
                        {"role": "assistant", "content": assistant_msg}
                    ]
                }
                outfile.write(json.dumps(chat_entry) + "\n")
                formatted_count += 1

    print(f"✅ Created {OUTPUT_FILE} with {formatted_count} conversational blocks.")

if __name__ == "__main__":
    transform_to_chatml()