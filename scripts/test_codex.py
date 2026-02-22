"""
================================================================
ZOMBIE WAVES AI CODEX: Inference & Validation (v2)
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
================================================================
"""

import os
import torch
from unsloth import FastLanguageModel
from datetime import datetime
import json
from config import EXT_MODEL_DIR, LOG_PATH, SYSTEM_PROMPT, MODEL_FOLDER, VERSION_NAME

MODEL_PATH = os.path.join(EXT_MODEL_DIR, MODEL_FOLDER)

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
    print(f"Loading Fine-Tuned Codex: {MODEL_PATH}")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = MODEL_PATH,
        max_seq_length = 512,
        load_in_4bit = True,
    )
    FastLanguageModel.for_inference(model)

    print(f"\nStarting Validation using Prompt Version: {VERSION_NAME}")
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
* **max_seq_length:** 512`
* **Gen Config:** `{json.dumps(GEN_CONFIG, indent=2)}
* **Prompt Version:** `{VERSION_NAME}`
* **Query:** {query}
* **Response:** > {response.strip()}
"""        

        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(log_entry)
        
        print(f"\n❓ QUERY: {query}")
        print(f"🤖 CODEX: {response.strip()}")

if __name__ == "__main__":
    run_validation()