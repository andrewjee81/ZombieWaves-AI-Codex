"""
Module: main.py
Project: ZombieWaves-AI-Codex
Description:
    The central orchestrator for the Project Codex data pipeline. 
    Sequentially executes sanitisation, pairing, and refinement to produce 
    a training-ready JSONL dataset from raw external drive snapshots.
Usage: python main.py
"""

import os
from scripts.sanitiser import sanitize_jsonl
from scripts.pairer import create_instruction_pairs
from _utils.refiner import refine_dataset

# 1. Define where the data lives (External Drive)
DATA_DIR = "/mnt/d/Project Codex"

# 2. Define the paths for our specific files
RAW_COMMENTS = os.path.join(DATA_DIR, "r_zombiewaves_comments.jsonl")
RAW_POSTS = os.path.join(DATA_DIR, "r_zombiewaves_posts.jsonl")

CLEAN_COMMENTS = os.path.join(DATA_DIR, "cleaned_comments.jsonl")
CLEAN_POSTS = os.path.join(DATA_DIR, "cleaned_posts.jsonl")

PAIRED_DATA = os.path.join(DATA_DIR, "paired_training_data.jsonl")
FINAL_REFINED_DATA = os.path.join(DATA_DIR, "refined_training_data.jsonl")

def main():
    print("--- 🧟 Project Codex: Automated Data Pipeline ---")
    
    # 1. Sanitisation: Remove PII and Noise
    print("\n[Step 1/3] Sanitising raw Reddit snapshots...")
    
    # Process Comments
    if os.path.exists(RAW_COMMENTS):
        sanitize_jsonl(RAW_COMMENTS, CLEAN_COMMENTS)
    else:
        print(f"❌ File not found: {RAW_COMMENTS}")

    # Process Posts
    if os.path.exists(RAW_POSTS):
        sanitize_jsonl(RAW_POSTS, CLEAN_POSTS)
    else:
        print(f"❌ File not found: {RAW_POSTS}")

    # 2. Pairing: Connect Questions to Expert Answers
    print("\n[Step 2/3] Pairing instructions with responses...")
    if os.path.exists(CLEAN_POSTS) and os.path.exists(CLEAN_COMMENTS):
        create_instruction_pairs(CLEAN_POSTS, CLEAN_COMMENTS, PAIRED_DATA)
    
    # 3. Refinement: De-duplication and Quality Filtering
    print("\n[Step 3/3] Refining dataset for AI training quality...")
    if os.path.exists(PAIRED_DATA):
        refine_dataset(PAIRED_DATA, FINAL_REFINED_DATA)
    
    print("\n✅ Pipeline Complete. Your training-ready dataset is at:")
    print(FINAL_REFINED_DATA)        

if __name__ == "__main__":
    main()