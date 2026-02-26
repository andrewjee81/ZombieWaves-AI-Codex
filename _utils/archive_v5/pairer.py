"""
Module: pairer.py
Project: ZombieWaves-AI-Codex
Description:
    The 'Matchmaker' script. It maps Reddit comments to their parent posts using
    optimised dictionary lookups. Transforms flat data into a Supervised 
    Fine-Tuning (SFT) format: Instruction-Response pairs.
Key Objective: Create the relational link between player questions and expert advice.
"""

import json
import os

def create_instruction_pairs(posts_path, comments_path, output_path):
    """
    Matches comments to their parent posts to create Instruction-Response pairs.
    """
    # 1. Build a "Knowledge Map" of Posts
    # Key: post_id | Value: post_text
    post_map = {}
    
    print("🧠 Loading posts into memory...")
    with open(posts_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            # Use 't3_' prefix if necessary, but Arctic Shift usually aligns these
            post_id = data.get("id")
            post_map[post_id] = data.get("text")

    print(f"✅ Loaded {len(post_map)} unique topics.")

    # 2. Match Comments to Posts
    print("🔗 Pairing comments with topics...")
    pair_count = 0
    
    with open(comments_path, 'r', encoding='utf-8') as f_in, \
         open(output_path, 'w', encoding='utf-8') as f_out:
        
        for line in f_in:
            comment_data = json.loads(line)
            parent_id = comment_data.get("parent_id")
            
            # Remove the Reddit prefix (e.g., 't3_') to match the ID
            if parent_id and "_" in parent_id:
                parent_id = parent_id.split("_")[1]

            # 3. If we find a match, create the pair
            if parent_id in post_map:
                pair = {
                    "instruction": post_map[parent_id], # The Question/Context
                    "response": comment_data.get("text") # The Expert Answer
                }
                
                # Only save if both sides have meaningful text
                if len(pair["instruction"]) > 10 and len(pair["response"]) > 10:
                    f_out.write(json.dumps(pair, ensure_ascii=False) + '\n') # OCD to correct encoded characters
                    pair_count += 1

    print(f"🚀 Success! Created {pair_count} Instruction-Response pairs.")

if __name__ == "__main__":
    # Standard paths for internal testing
    create_instruction_pairs(
        '/mnt/d/Project Codex/cleaned_posts.jsonl',
        '/mnt/d/Project Codex/cleaned_comments.jsonl',
        '/mnt/c/inetpub/wwwroot/GitHub/ZombieWaves-AI-Codex/data/reddit_paired_data.jsonl'
    )