"""
Module: sanitiser.py
Project: ZombieWaves-AI-Codex
Description:
    Processes raw Reddit snapshots to remove PII (Personally Identifiable Information).
    Filters out 'deleted' or 'removed' content and applies a blacklist of post IDs
    to respect user 'Right to Erasure' requests.
Key Objective: Anonymise data while preserving strategic game context.
"""

import json
import os

def sanitise_jsonl(input_path, output_path, blacklist_path=None):
    """
    Reads raw Reddit JSONL data and strips PII (usernames/IDs).
    """
    # 1. Load the blacklist if it exists
    blacklist = set()
    if blacklist_path and os.path.exists(blacklist_path):
        with open(blacklist_path, 'r') as f:
            blacklist = {line.strip() for line in f if line.strip()}

    print(f"Filtering: {input_path}")
    
    processed_count = 0
    skipped_count = 0

    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            try:
                data = json.loads(line)
                
                # 2. Check Blacklist (Right to Erasure)
                # If the post ID is in our blacklist, we skip the whole line
                if data.get('id') in blacklist:
                    skipped_count += 1
                    continue
                
                # 3. PII Stripping (The "Anonymizer")
                # We create a NEW dictionary containing ONLY what we need.
                # We completely ignore 'author', 'author_fullname', etc.
                clean_entry = {
                    "id": data.get("id"),
                    "parent_id": data.get("parent_id"), # Needed to link comments to posts
                    "text": data.get("body") or data.get("selftext"), # Comments use 'body', Posts use 'selftext'
                    "score": data.get("score")
                }

                # 4. Final Validation
                # Only save if there is actually text to read
                if clean_entry["text"] and clean_entry["text"] != "[deleted]":
                    outfile.write(json.dumps(clean_entry, ensure_ascii=False) + '\n')
                    processed_count += 1
                else:
                    skipped_count += 1

            except json.JSONDecodeError:
                continue

    print(f"✅ Success! Processed: {processed_count} | Skipped/Blacklisted: {skipped_count}")

if __name__ == "__main__":
    # Test run logic
    sanitize_jsonl('/mnt/d/Project Codex/r_zombiewaves_comments.jsonl', '/mnt/d/Project Codex/cleaned_comments.jsonl')