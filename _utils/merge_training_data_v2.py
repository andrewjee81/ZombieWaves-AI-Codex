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
from pathlib import Path

SYSTEM_PROMPT = (
    "You are the Zombie Waves AI Codex, an expert strategy assistant specializing in gear optimization, "
    "trait stacking logic, and high-efficiency build architecture. "
    "Your goal is to provide accurate, concise, and helpful gameplay advice for Zombie Waves. "
    "Stay in character and only discuss Zombie Waves content."
)

GOLD_SOURCES = ['master_codex.jsonl','zombie_waves_pdf_codex_STRATEGY_ONLY.jsonl']
SILVER_SOURCES = ['zombie_waves_reddit_filtered.jsonl','zombie_waves_discord_chatml_filtered.jsonl','zombie_waves_youtube_chatml.jsonl']
OUTPUT_FILE = Path('./data') / 'training_master_v2_weighted.jsonl'
GOLD_WEIGHT = 5

def process_line(line):
    """Parses a line and ensures the system prompt is updated to the latest version."""
    data = json.loads(line)
    # Update the system message to ensure consistency across all sources
    for message in data['messages']:
        if message['role'] == 'system':
            message['content'] = SYSTEM_PROMPT
    return data

def merge_datasets():
    final_data = []
    print("🚀 Starting Unified Weighted Merger...")

    # Process GOLD (5x)
    for source in GOLD_SOURCES:
        source = Path('./data') / source

        if os.path.exists(source):
            with open(source, 'r', encoding='utf-8') as f:
                samples = [process_line(line) for line in f]
                for _ in range(GOLD_WEIGHT):
                    final_data.extend(samples)
            print(f"✔ Weighted 5x: {source}")

    # Process SILVER (1x)
    for source in SILVER_SOURCES:
        source = Path('./data') / source
        
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