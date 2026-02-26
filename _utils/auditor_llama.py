"""
================================================================
ZOMBIE WAVES AI CODEX: LLAMA-POWERED DATA AUDITOR
================================================================
ROLE:         AI Quality Control (Judge Model)
ENGINE:       Llama-3.2-3B-Instruct (4-bit Unsloth)
PURPOSE:      Semantic filtering of Reddit & Discord data.
              Removes 'Trash' (social noise, complaints) and 
              identifies 'Mechanical Conflicts' (EoH + Miniclip).
OUTPUT:       Clean JSONL pairs for merge_training_data_v2.py
================================================================
"""

import sys
import os
import json
import torch
from pathlib import Path
from tqdm import tqdm
from unsloth import FastLanguageModel

# Path Injection: Allow script to import from root directory
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import VERSION_NAME, IDENTITY, LOCAL_DATA_DIR

# 1. Load the Model
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Llama-3.2-3B-Instruct-bnb-4bit",
    max_seq_length = 2048,
    load_in_4bit = True,
)
FastLanguageModel.for_inference(model)
"""
SYSTEM_PROMPT = (
    "You are an expert data auditor for the Zombie Waves AI Codex. Your task is to classify text as 'STRATEGY' or 'TRASH'. "
    "1. STRATEGY: Technical game mechanics, weapon builds, or stage tactics. Include: 'Windborne Boost', "
    "fire-rate synergies for EoH, or MX/FM frost builds. Rule: Save ANY technical advice, even if it doesn't "
    "mention these specific examples. 2. TRASH: Social chatter, 'thank you' notes, gacha complaints, or generic "
    "low-effort questions. 3. CONFLICT: Mechanical Disruption. Use this for advice that breaks core synergies. "
    "Example: Suggesting 'Miniclip' or 'Reload' for 'Eye of the Hurricane' (EoH) is TRASH because it disrupts the "
    "50-shot Vortex trigger."
)
"""
SYSTEM_PROMPT = """You are a Senior Strategy Editor for Zombie Waves. 
Your task is to take a Discord conversation pair and DISTILL it into a permanent strategy entry.

RULES:
1. STRIP SOCIAL NOISE: Remove "lol", "congrats", "thanks", "nice", and personal anecdotes.
2. TECHNICAL ONLY: If the pair doesn't contain a specific trait, weapon name, or mechanical value, mark as TRASH.
3. ROLE SWAP: If the 'User' provided the tip and the 'Assistant' just said "thanks", SWAP the roles so the tip is in the Assistant's mouth.
4. IMAGE AWARENESS: If [Image Attached] is present, ensure the Assistant describes the technical context (e.g., "This build focuses on...") instead of just acknowledging the image.

"""

def audit_entry(messages):
    """
    Evaluates if the content is high-quality strategy or social noise.
    """
    # Extract content for the prompt
    user_q = messages[1]['content']
    asst_a = messages[2]['content']
    
    # PRE-TRUNCATION: Slice characters to stay well under the 2048 token limit
    # This prevents the 'Input IDs > 2048' error and keeps VRAM at ~3.8GB
    user_q_snippet = user_q[:1200] 
    asst_a_snippet = asst_a[:3000]  

    # SYSTEM PROMPT FOR AUDITOR    
    prompt = (
        f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
        f"{SYSTEM_PROMPT}\n"
        f"TEXT TO AUDIT:\nUSER: {user_q_snippet}\nASSISTANT: {asst_a_snippet}\n\n"
        f"Response (STRATEGY or TRASH):<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"
    )

    # FIX: Using proper padding and attention masks to prevent truncated/corrupted outputs
    inputs = tokenizer([prompt], return_tensors = "pt", padding=True, truncation=True).to("cuda")
    
    outputs = model.generate(
        **inputs, 
        max_new_tokens = 10, 
        use_cache = True,
        pad_token_id = tokenizer.eos_token_id # Ensures generation stops correctly
    )
    
    # Extract only the newly generated text
    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    verdict = decoded.split("assistant")[-1].strip().upper()
    
    return "STRATEGY" in verdict

# 2. File Processing
input_file = os.path.join(LOCAL_DATA_DIR, 'zombie_waves_discord_final_gold_v2.jsonl')
output_file = os.path.join(LOCAL_DATA_DIR, 'zombie_waves_discord_final_gold_v3.jsonl')

print(f"--- STARTING AI AUDIT: {IDENTITY} [{VERSION_NAME}] ---")
print(f"--- VRAM STATUS: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f}GB Detected ---")

kept = 0
deleted = 0

if not os.path.exists(input_file):
    print(f"Error: {input_file} not found.")
    sys.exit()

with open(input_file, 'r', encoding='utf-8') as f_in, \
     open(output_file, 'w', encoding='utf-8') as f_out:
    
    lines = f_in.readlines()
    for line in tqdm(lines, desc="Auditing Data"):
        try:
            data = json.loads(line)
            if audit_entry(data['messages']):
                f_out.write(json.dumps(data) + '\n')
                kept += 1
            else:
                deleted += 1
        except Exception as e:
            print(f"Skip error: {e}")
            continue

print(f"\nAudit Complete! Kept: {kept} | Deleted: {deleted}")