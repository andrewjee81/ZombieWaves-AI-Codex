import json
import re

input_file = './data/zombie_waves_reddit_chatml.jsonl'
output_file = './data/zombie_waves_reddit_filtered.jsonl'

# PROTECT: Keywords that prove the entry contains real strategy
protect_keys = ["tier", "rank", "vs", "better", "best", "priority", "stats", "build", 
                "weapon", "gear", "robot", "stage", "damage", "attack", "crit", 
                "voltgun", "arbalest", "boreas", "rpg", "meteor", "hero", "blueprint"]

# BURN: Keywords that identify useless Reddit/Social noise
burn_keys = ["post", "reddit", "sub", "edit:", "tldr", "upvote", "link", "photo", 
             "image", "thread", "customer support", "review", "star", "redeem code"]

kept = 0
deleted = 0

with open(input_file, 'r', encoding='utf-8') as f_in, \
     open(output_file, 'w', encoding='utf-8') as f_out:
    
    for line in f_in:
        data = json.loads(line)
        assistant = data['messages'][2]['content'].lower()
        user = data['messages'][1]['content'].lower()
        combined = user + " " + assistant
        
        # LOGIC:
        # 1. If it contains BURN keys and NO PROTECT keys -> DELETE
        # 2. If it is too short (< 10 words) and NO PROTECT keys -> DELETE
        # 3. Otherwise -> KEEP
        
        has_burn = any(k in combined for k in burn_keys)
        has_protect = any(k in combined for k in protect_keys)
        is_short = len(assistant.split()) < 10
        
        if (has_burn and not has_protect) or (is_short and not has_protect):
            deleted += 1
        else:
            f_out.write(line)
            kept += 1

print(f"Reddit Cleanup Complete!")
print(f"Kept: {kept} High-Signal Entries")
print(f"Deleted: {deleted} Low-Signal Noise Entries")