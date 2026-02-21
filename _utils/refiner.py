"""
Module: refiner.py
Project: ZombieWaves-AI-Codex
Description:
    Performs data science optimisations on paired data. Uses fingerprint hashing
    to remove duplicate entries and applies heuristic length filters to purge
    low-signal responses (social filler).
Key Objective: Maximise the signal-to-noise ratio for higher-quality AI training.
"""

import json

def refine_dataset(input_path, output_path):
    unique_pairs = set()
    final_data = []
    
    print(f"🧐 Refining 17,014 pairs for quality...")

    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            pair = json.loads(line)
            # Create a unique "fingerprint" of the instruction and response
            # This catches exact duplicates even if they have different IDs
            fingerprint = (pair['instruction'].strip(), pair['response'].strip())

            if fingerprint not in unique_pairs:
                # Quality Check: Ensure the response is long enough to be helpful
                if len(pair['response'].split()) > 3: 
                    unique_pairs.add(fingerprint)
                    final_data.append(pair)

    with open(output_path, 'w', encoding='utf-8') as f_out:
        for entry in final_data:
            f_out.write(json.dumps(entry, ensure_ascii=False) + '\n')

    print(f"✨ Refinement complete! Removed {17014 - len(final_data)} redundant pairs.")
    print(f"📊 Final high-quality count: {len(final_data)}")

if __name__ == "__main__":
    refine_dataset('/mnt/d/Project Codex/final_training_data.jsonl', 
                   '/mnt/d/Project Codex/refined_training_data.jsonl')