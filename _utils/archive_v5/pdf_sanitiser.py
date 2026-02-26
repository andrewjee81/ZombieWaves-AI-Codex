import json

input_file = './data/zombie_waves_pdf_codex_chatml_refined.jsonl'
output_file = './data/zombie_waves_pdf_codex_STRATEGY_ONLY.jsonl'

# Keywords that identify the "Event Math" sections
event_junk = ["draws:", "tickets from", "daily ads", "battle pass", "shopping carts", "¥", "diamond use"]

kept = 0
deleted = 0

with open(input_file, 'r', encoding='utf-8') as f_in, \
     open(output_file, 'w', encoding='utf-8') as f_out:
    for line in f_in:
        data = json.loads(line)
        content = data['messages'][2]['content'].lower()
        
        # If it mentions currency or draw-math, it's likely the event calculation section
        if any(k in content for k in event_junk):
            deleted += 1
        else:
            f_out.write(line)
            kept += 1

print(f"Cleanup Complete! Strategy Kept: {kept}, Event Math Deleted: {deleted}")