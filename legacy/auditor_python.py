import json
import re
import sys
import os
from pathlib import Path

# Path Injection: Allow script to import from root directory
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import VERSION_NAME, IDENTITY, LOCAL_DATA_DIR

print(f"--- STARTING AI AUDIT: {IDENTITY} [{VERSION_NAME}] ---")

input_file = os.path.join(LOCAL_DATA_DIR, 'zombie_waves_discord_chatml_refined.jsonl')
output_file = os.path.join(LOCAL_DATA_DIR, 'zombie_waves_discord_final_gold_py.jsonl')


# 1. PROTECT: High-signal markers (Don't delete if these are here)
protect_keys = ["tier", "rank", "vs", "priority", "stats", "build", "weapon", "gear", 
                "voltgun", "arbalest", "boreas", "rpg", "meteor", "hero", "blueprint",
                "miniclip", "eoh", "windborne", "shatter", "modified xyclon", "mx"]

# 2. BURN: Low-signal noise (Delete if no protect keys found)
burn_keys = ["post", "reddit", "sub", "edit:", "tldr", "upvote", "link", "photo", 
             "image", "thread", "customer support", "review", "star", "redeem code",
             "pity", "greedy", "scam", "quit", "devs",
             "dm me", "discord", "server", "channel", "slightly_smiling_face", 
             "sparkles", "lmao", "lol", "message me"]

# 3. BRITISH DICTIONARY: Regional enforcement
british_map = {
    r"\barmor\b": "armour",
    r"\bspecializing\b": "specialising",
    r"\bprioritize\b": "prioritise",
    r"\bdefense\b": "defence",
    r"\bprogram\b": "programme",
    r"\banalyze\b": "analyse",
    r"\bcolor\b": "colour",
    r"\boptimized\b": "optimised"
}

def clean_and_sanitise(text):
    # Strip "Reddit-speak" and first-person fluff
    text = re.sub(r'\b(i think|i believe|in my opinion|to be honest|imo|imho|hey|hi|thanks)\b', '', text, flags=re.IGNORECASE)
    
    # Force British English
    for us_regex, uk_word in british_map.items():
        text = re.sub(us_regex, uk_word, text, flags=re.IGNORECASE)
    
    # MECHANICAL CONFLICT GUARD: The "Anti-Ammu" logic
    # If the text suggests Miniclip/Ammu for EoH, we neutralize the advice or flag for deletion
    if "eoh" in text.lower() and ("miniclip" in text.lower() or "single shot" in text.lower()):
        return None # Effectively deletes this line from training
    
    # Cleanup spacing
    text = " ".join(text.split()).strip()
    if len(text) > 2:
        text = text[0].upper() + text[1:]
    return text

kept = 0
deleted = 0

with open(input_file, 'r', encoding='utf-8') as f_in, \
     open(output_file, 'w', encoding='utf-8') as f_out:
    
    for line in f_in:
        data = json.loads(line)
        user_msg = data['messages'][1]['content'].lower()
        asst_msg = data['messages'][2]['content']
        
        combined = (user_msg + " " + asst_msg).lower()
        
        has_burn = any(k in combined for k in burn_keys)
        has_protect = any(k in combined for k in protect_keys)
        
        # Filtering Logic
        if (has_burn and not has_protect) or len(asst_msg.split()) < 8:
            deleted += 1
            continue
        
        # Sanitisation Logic
        sanitised_content = clean_and_sanitise(asst_msg)
        
        if sanitised_content is None or len(sanitised_content) < 10:
            deleted += 1
            continue

        data['messages'][2]['content'] = sanitised_content
        f_out.write(json.dumps(data) + '\n')
        kept += 1

print(f"Cleanup Complete! Kept: {kept} | Deleted: {deleted}")