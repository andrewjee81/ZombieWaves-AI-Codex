"""
================================================================
ZOMBIE WAVES AI CODEX: DISCORD CONVERSATION FLATTENER (v1.5)
================================================================
FILE DESCRIPTION: 
This script flattens the nested 'conversations' output from the 
clean-discord script. It converts escaped newlines into real 
line breaks and uses a double-newline separator to preserve 
the conversational flow of multi-message expert advice blocks, 
allowing the Llama Auditor to see the full context of a tip.
================================================================
"""

import json
import os
from pathlib import Path
import sys

# Adjust path to import from your project root
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from config import LOCAL_DATA_DIR, SYSTEM_PROMPT

# CONFIGURATION
# Input should be the JSON file produced by DiscordChatExporter
INPUT_FILE = os.path.join(LOCAL_DATA_DIR, "Discord_cleaned.json") 
OUTPUT_FILE = os.path.join(LOCAL_DATA_DIR, "discord_final_chatml.jsonl")

def process_cleaned_discord():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: {INPUT_FILE} not found.")
        return

    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ JSON Load Error: {e}")
        return

    conversations = data.get('conversations', [])
    print(f"📦 Processing {len(conversations)} conversation blocks...")

    chatml_entries = []

    for conv in conversations:
        if not conv:
            continue

        processed_msgs = []
        for msg_pair in conv:
            # clean-discord format: ["Username: Content", "UserID"]
            full_text = msg_pair[0]
            
            # Step 1: Strip username
            if ': ' in full_text:
                clean_content = full_text.split(': ', 1)[1]
            else:
                clean_content = full_text

            # Step 2: Fix escaped newlines (\n -> actual newline)
            clean_content = clean_content.replace("\\n", "\n")
            
            processed_msgs.append(clean_content.strip())

        if not processed_msgs:
            continue

        # Turn 0 is the "User" (the person who started the topic/asked the question)
        user_input = processed_msgs[0]
        
        # All subsequent messages are the "Assistant" (the expert responses)
        # We join with \n\n to maintain the "chat transcript" look
        if len(processed_msgs) > 1:
            assistant_output = "\n\n".join(processed_msgs[1:])
        else:
            assistant_output = "[Direct Strategy Entry]"

        entry = {
            "messages": [
                {
                    "role": "system", 
                    "content": SYSTEM_PROMPT
                },
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": assistant_output}
            ]
        }
        chatml_entries.append(entry)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f_out:
        for entry in chatml_entries:
            f_out.write(json.dumps(entry, ensure_ascii=False) + '\n')

    print(f"✅ Success! Conversational blocks preserved in ChatML.")

if __name__ == "__main__":
    process_cleaned_discord()