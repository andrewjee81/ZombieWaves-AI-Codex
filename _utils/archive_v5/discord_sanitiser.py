import json

input_file = './data/zombie_waves_discord_chatml.jsonl'
output_file = './data/zombie_waves_discord_chatml_refined.jsonl'

# High-priority keywords that save a line from deletion
priority_keywords = [
    # General Meta
    "hero", "weapon", "robot", "trait", "blueprint", "module", "vb", "virtual",
    "conquest", "build", "strategy", "pants", "suit", "boots", "insignia", 
    "pendant", "damage", "attack", "crit", "reload", "projectile", "tier",
    # Specific High-Value Bots/Weapons
    "skylark", "reindeer", "penguin", "ullr", "calamity", "pyreon", "snorf",
    "voltgun", "voltstrike", "arbalest", "meteor", "boreas", "xyclon", "balrog",
    # Specific Stages/Modes
    "testworks", "arena", "guild", "checkpoint", "stage", "wave"
]

kept_count = 0
deleted_count = 0

with open(input_file, 'r', encoding='utf-8') as f_in, \
     open(output_file, 'w', encoding='utf-8') as f_out:
    
    for line in f_in:
        data = json.loads(line)
        content = data['messages'][2]['content'].lower()
        word_count = len(content.split())
        
        # LOGIC:
        # 1. If it's the Hero Guide data we made (User query starts with "How should I build") -> KEEP
        # 2. If it contains priority keywords -> KEEP
        # 3. If it's just chatter but very long (might have hidden advice) -> KEEP
        # 4. Otherwise -> DELETE
        
        is_hero_guide = "how should i build" in data['messages'][1]['content'].lower()
        has_priority = any(k in content for k in priority_keywords)
        
        if is_hero_guide or has_priority or word_count > 25:
            f_out.write(line)
            kept_count += 1
        else:
            deleted_count += 1

print(f"Filtering Complete!")
print(f"Kept: {kept_count} (High Quality)")
print(f"Deleted: {deleted_count} (Low Quality Noise)")