"""
================================================================
ZOMBIE WAVES AI CODEX: DATA QUALITY BENCHMARK (v6.1)
================================================================
ROLE:         Comparative Auditor (Logic Validator)
ENGINE:       Python (Set Theory & Overlap Analysis)
PURPOSE:      Benchmarks Regex Sanitiser vs. AI Judge.
              Identifies 'False Positives' and 'Missed Signal'.
================================================================
"""

import json

# Define your paths
REGEX_FILE = './data/zombie_waves_discord_final_gold_py.jsonl'
AI_FILE = './data/zombie_waves_discord_final_gold.jsonl'

def load_ids(file_path):
    # Using the assistant content as a unique hash (or ID) for comparison
    ids = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            # We use a hash of the user message to identify the specific entry
            msg_id = hash(data['messages'][1]['content'])
            ids[msg_id] = data['messages'][2]['content']
    return ids

print("--- STARTING DATASET COMPARISON ---")

regex_data = load_ids(REGEX_FILE)
ai_data = load_ids(AI_FILE)

regex_set = set(regex_data.keys())
ai_set = set(ai_data.keys())

# Logic Overlap
both_kept = regex_set.intersection(ai_set)
regex_only = regex_set - ai_set
ai_only = ai_set - regex_set  # This should be 0 if AI only filters the regex output

print(f"\n[BENCHMARK STATS]")
print(f"Total entries in Regex set: {len(regex_set)}")
print(f"Total entries in AI set:    {len(ai_set)}")
print(f"Overlap (Agreed):           {len(both_kept)}")
print(f"Regex Only (AI Deleted):    {len(regex_only)}")

print(f"\n--- SAMPLES: AI-DELETED ENTRIES (The 'Trash' the AI caught) ---")
# Show 3 examples of what the AI deleted that Regex missed
for i, msg_id in enumerate(list(regex_only)[:3]):
    print(f"\nSample {i+1}:")
    print(f"Content: {regex_data[msg_id][:150]}...")

print("\n--- END OF COMPARISON ---")