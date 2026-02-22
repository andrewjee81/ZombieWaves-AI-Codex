"""
Master Training Merger (v2)
================================================================
DESCRIPTION:
This script consolidates multi-source JSONL datasets into a single 
training master file. It applies strategic "Authority Weighting" 
to prioritize verified game mechanics over community chatter.

KEY ARCHITECTURAL FEATURES:
1. Unified Persona: Injects the latest System Prompt into every sample.
2. Authority Weighting: 5x Oversampling for Gold Standard sources 
   (In-Game Codex & Veteran PDF) to ensure expert-level logic.
3. Signal Cleaning: Standardizes formatting across Reddit/Discord sources.
4. Strategic Shuffle: Ensures the "Long Burn" (1,200 steps) encounters 
   authoritative facts consistently throughout the training run.

DATA FORMAT: ChatML (System, User, Assistant)
================================================================
"""

import json
import random
import os
import re
from pathlib import Path
from config import LOCAL_DATA_PATH, SYSTEM_PROMPT, VERSION

GOLD_SOURCES = ['master_codex.jsonl']
SILVER_SOURCES = ['zombie_waves_reddit_filtered.jsonl','zombie_waves_discord_chatml_refined.jsonl']
OUTPUT_FILE = LOCAL_DATA_PATH / f'training_master_v{VERSION}_weighted.jsonl'
GOLD_WEIGHT = 5

def process_line(line):
    """Parses a line and ensures the system prompt is updated to the latest version."""
    data = json.loads(line)
    # Update the system message to ensure consistency across all sources
    for message in data['messages']:
        if message['role'] == 'system':
            message['content'] = SYSTEM_PROMPT

            # Strip Urls and clean newlines
            message['content'] = re.sub(r'https?://\S+', '', message['content'])
            message['content'] = message['content'].replace('\n', ' ').replace('\r', '')
    return data

def merge_datasets():
    final_data = []
    print("🚀 Starting Unified Weighted Merger...")

    # Process GOLD (5x)
    for source in GOLD_SOURCES:
        source = LOCAL_DATA_PATH / source

        if os.path.exists(source):
            with open(source, 'r', encoding='utf-8') as f:
                samples = [process_line(line) for line in f]
                for _ in range(GOLD_WEIGHT):
                    final_data.extend(samples)
            print(f"✔ Weighted 5x: {source}")

    # Process SILVER (1x)
    for source in SILVER_SOURCES:
        source = LOCAL_DATA_PATH / source
        
        if os.path.exists(source):
            with open(source, 'r', encoding='utf-8') as f:
                samples = [process_line(line) for line in f]
                final_data.extend(samples)
            print(f"✔ Weighted 1x: {source}")

    # Shuffle & Save
    random.shuffle(final_data)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for entry in final_data:
            f.write(json.dumps(entry) + '\n')

    print(f"✅ Final file created: {OUTPUT_FILE} ({len(final_data)} total samples)")

if __name__ == "__main__":
    merge_datasets()