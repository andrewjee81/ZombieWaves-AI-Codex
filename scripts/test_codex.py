"""
🚀 PROJECT: Zombie Waves AI Codex - Inference & Validation (v2)
================================================================
DESCRIPTION:
This script serves as the primary validation gate for the 
'Long Burn' fine-tune. It tests the model's ability to recall 
high-density strategy logic from the master hero data and 
PDF strategy guides over general community chatter.

VALIDATION METRICS:
1. Technical Precision: Does the model correctly name traits/gear?
2. Reasoning Alignment: Does it follow the 5x weighted veteran logic?
3. Persona Integrity: Does it maintain the 'Expert Strategy Assistant' tone?

TARGET MODEL: final_codex_model_v2 (Step 1200 / Loss 1.78)
HARDWARE: NVIDIA RTX 3050 (4GB VRAM)
================================================================
"""

import os
import torch
from unsloth import FastLanguageModel
from datetime import datetime

# --- CONFIGURATION & VERSIONING ---
MODEL_PATH = "/mnt/d/Project Codex/ZombieWaves-AI-Codex-Train/final_codex_model_v2"
LOG_FILE_PATH = "/mnt/c/inetpub/wwwroot/GitHub/ZombieWaves-AI-Codex/docs/training_log.md"

# ================================================================
# ⚙️ MASTER CONFIGURATION: ZOMBIE WAVES AI CODEX (v2.2)
# ================================================================
# This configuration is tuned to suppress "Silver" Reddit noise
# and prioritize "Gold" PDF strategy logic (Step 1200 / Loss 1.78).
PROMPT_VERSION = "v2.2 (Exploit-Aware & Anti-Stutter)"

SYSTEM_PROMPT = (
    "You are the Zombie Waves AI Codex, a technical strategy engine. "
    "Your objective is to provide high-level synergies including 'Infinite Ammo' exploits and 'Last Shot' procs. "
    "\n\nCRITICAL CONSTRAINTS:"
    "\n- NEVER use first-person language (No 'I', 'me', 'my')."
    "\n- STOP word repetitions (No double names like 'Edge's Edge')."
    "\n- FOCUS on mechanics: Miniclip, Entrenched, and Reload-based triggers."
    "\n- If Arbalest is mentioned with MX, prioritize 'Infinite Ammo' loop logic."
)

# 🧪 OPTIMIZED GENERATION HYPERPARAMETERS
GEN_CONFIG = {
    "max_new_tokens": 256,
    "temperature": 0.35,           # Low temp = High precision
    "top_p": 0.9,                  # Narrative filtering
    "repetition_penalty": 1.2,     # Anti-stutter mechanism
    "do_sample": True,
    "use_cache": True,
}
# ================================================================

# 🎯 TEST CASES
TEST_QUERIES = [
    "What is the optimal trait stacking logic for the Frostfall Rocket Launcher?",
    "How should I build Modified Xyclon (MX) for high-efficiency stage clearing?",
    "Which robots provide the best synergy for a Voltgun build?",
    "Explain the 'Veteran' approach to boss tactics in the late-game stages.",
    "What are the traits to use for Arbalest when paired with MX?"
]

def run_validation():
    print(f"📦 Loading Fine-Tuned Codex: {MODEL_PATH}")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = MODEL_PATH,
        max_seq_length = 2048,
        load_in_4bit = True,
    )
    FastLanguageModel.for_inference(model)

    print(f"\n🚀 Starting Validation using Prompt Version: {PROMPT_VERSION}")
    print("-" * 30)

    for query in TEST_QUERIES:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ]
        
        inputs = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt = True,
            return_tensors = "pt",
            return_dict = True,
        ).to("cuda")

        outputs = model.generate(
            **inputs, 
            **GEN_CONFIG,
            pad_token_id = tokenizer.eos_token_id
        )
        
        input_length = inputs["input_ids"].shape[1]
        response = tokenizer.batch_decode(outputs[:, input_length:], skip_special_tokens=True)[0]

        # Log to Markdown with Metadata
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"""
---
### 🧪 Inference Test: {timestamp}
* **Model:** `{os.path.basename(MODEL_PATH)}`
* **Prompt Version:** `{PROMPT_VERSION}`
* **Query:** {query}
* **Response:** > {response.strip()}
"""        

        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(log_entry)
        
        print(f"\n❓ QUERY: {query}")
        print(f"🤖 CODEX: {response.strip()}")

if __name__ == "__main__":
    run_validation()