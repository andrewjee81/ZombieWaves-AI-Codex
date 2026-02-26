"""
================================================================
ZOMBIE WAVES AI CODEX: LLAMA-POWERED DATA AUDITOR (v6.2.2)
================================================================
ROLE:         AI Quality Control (Judge Model)
ENGINE:       Llama-3.2-3B-Instruct (4-bit Unsloth)
PURPOSE:      Semantic filtering of Reddit & Discord data.
              Removes 'Trash' (social noise, complaints) and 
              identifies 'Mechanical Conflicts' (EoH + Miniclip).
OUTPUT:       Clean JSONL pairs for merge_training_data_v2.py
================================================================
"""

import os
import sys
import json
import torch
from pathlib import Path
from tqdm import tqdm
from unsloth import FastLanguageModel

# 1. Environment & Path Setup
# Silences the nightly version mismatch warning for your 3050 rig
os.environ["UNSLOTH_SKIP_TORCHVISION_CHECK"] = "1"
os.environ["UNSLOTH_SKIP_COMPILER"] = "1"

# Adjust path to import from your project root
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import VERSION_NAME, IDENTITY, LOCAL_DATA_DIR

# 2. Load the Model (Optimised for 4GB VRAM)
MODEL_NAME = "unsloth/Llama-3.2-3B-Instruct-bnb-4bit"
MAX_SEQ_LENGTH = 2048 

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = MODEL_NAME,
    max_seq_length = MAX_SEQ_LENGTH,
    load_in_4bit = True,
)
FastLanguageModel.for_inference(model)

def audit_entry(instruction, response):
    """
    Evaluates if content is technical game intel or social noise.
    """
    if not instruction or not response:
        return "TRASH", False

    # Precision Prompt for both Reddit (QA) and Discord (Chat)
    system_prompt = (
        "You are the Zombie Waves AI Quality Auditor. Your goal is to separate 'Silver Truths' from 'Trash'.\n\n"
        "--- CORE CLASSIFICATION RULES ---\n"
        "1. [STRATEGY]: Technical game mechanics, expert builds, or gear advice. \n"
        "   *SAVE IF*: Mentions 'Windborne Boost' (Storm/Dodge tree), fire-rate synergies for Eye of the Hurricane (EoH), "
        "   or MX/FM frost builds.\n"
        "2. [CONFLICT]: Mechanical anti-synergy. Specifically, if a post suggests 'Miniclip' or 'Reload' "
        "   trees for Eye of the Hurricane (EoH), mark as [CONFLICT].\n"
        "   *LOGIC*: EoH triggers a Vortex every 50 shots. Miniclip sets ammo to 1, making the Vortex impossible to sustain.\n"
        "3. [TRASH]: Social noise, 'thank you' notes, gacha pull complaints, emojis, or low-effort chatter.\n\n"
        "--- DECISION LOGIC ---\n"
        "- If [CONFLICT] is detected, treat as TRASH for the Codex.\n"
        "- Respond ONLY with: [STRATEGY], [CONFLICT], or [TRASH]."
    )

    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>
DATA:
Input: {instruction[:500]}
Output: {response[:1000]}

CLASSIFICATION:<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

    inputs = tokenizer([prompt], return_tensors="pt").to("cuda")
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs, 
            max_new_tokens=12, 
            use_cache=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    # Decode only the assistant's new tokens
    decoded = tokenizer.batch_decode(outputs[:, inputs.shape[1]:], skip_special_tokens=True)[0]
    verdict = decoded.strip().upper()
    
    # Keep if it is mechanical intel or strategy
    is_useful = "[CONFLICT]" in verdict or "[STRATEGY]" in verdict or "STRATEGY" in verdict or "CONFLICT" in verdict
    return verdict, is_useful

# 3. Main Processing Loop
def run_audit(input_filename, output_filename):
    input_path = os.path.join(LOCAL_DATA_DIR, input_filename)
    output_path = os.path.join(LOCAL_DATA_DIR, output_filename)
    
    print(f"--- STARTING UNIFIED AUDIT (v6.2) ---")
    print(f"Target: {input_filename} -> {output_filename}")
    
    kept, deleted = 0, 0

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    with open(input_path, 'r', encoding='utf-8') as f_in, \
         open(output_path, 'w', encoding='utf-8') as f_out:
        
        lines = f_in.readlines()
        for line in tqdm(lines, desc="Auditing"):
            try:
                data = json.loads(line)
                
                # Dynamic Key Extraction (Handles pairer.py and Discord ChatML)
                # If it's a ChatML 'messages' list, we extract user/assistant text
                if "messages" in data:
                    inst = data["messages"][1]["content"] if len(data["messages"]) > 1 else ""
                    resp = data["messages"][2]["content"] if len(data["messages"]) > 2 else ""
                else:
                    inst = data.get("instruction") or data.get("prompt") or ""
                    resp = data.get("response") or data.get("content") or ""

                label, is_gold = audit_entry(inst, resp)

                if is_gold:
                    # Output in standard Instruction/Response for merger_training_data_v2.py
                    clean_output = {
                        "instruction": inst,
                        "response": resp,
                        "audit_label": label  # Helpful for spot-checking
                    }
                    f_out.write(json.dumps(clean_output, ensure_ascii=False) + '\n')
                    kept += 1
                else:
                    deleted += 1
            except Exception as e:
                continue

    print(f"\n✅ Audit Finished: {kept} kept, {deleted} removed.")

if __name__ == "__main__":
    print(f"--- STARTING AI AUDIT: {IDENTITY} [{VERSION_NAME}] ---")
    print(f"--- VRAM STATUS: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f}GB Detected ---")
    run_audit('reddit_paired_data.jsonl', 'zombie_waves_reddit_final_gold.jsonl')