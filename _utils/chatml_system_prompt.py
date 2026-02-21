import json

target_prompt = (
    "You are the Zombie Waves AI Codex, an expert strategy assistant specializing in gear optimization, "
    "trait stacking logic, and high-efficiency build architecture. "
    "Your goal is to provide accurate, concise, and helpful gameplay advice for Zombie Waves. "
    "Stay in character and only discuss Zombie Waves content."
)

total_lines = 0

with open('./data/zombie_waves_master_codex.jsonl', 'r') as f, \
     open('./data/zombie_waves_master_codex_chatml_final.jsonl', 'w') as out:
    for line in f:
        data = json.loads(line)
        # Standardize the first message (system role)
        data['messages'][0]['content'] = target_prompt
        out.write(json.dumps(data) + '\n')
        total_lines += 1