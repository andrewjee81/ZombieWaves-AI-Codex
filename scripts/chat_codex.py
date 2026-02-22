"""
================================================================
ZOMBIE WAVES AI CODEX: VETERAN INFERENCE ENGINE (v6.1)
================================================================
ARCHITECTURE: Llama-3.2-3B-Instruct (Unsloth 4-bit)
DNA MARKERS:  Exploit-Aware, Anti-Stutter, British English Meta
================================================================
DESCRIPTION:
This script facilitates real-time interaction with the fine-tuned 
v6.1 adapter. It leverages the "Gold Truth" knowledge base to 
provide mechanical denials (e.g., EoH/Miniclip separation) and 
high-tier progression strategy.

SYSTEM STATE:
- Persona: Veteran Strategy Engine (Static Enforcement)
- Logic:   Gold Truth Anchored (5:1 Weighted Data)
- Meta:    2026 Global Version
================================================================
"""

import torch
import os
import json
from datetime import datetime
from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template
from config import LOG_PATH, MODEL_PATH, SYSTEM_PROMPT, VERSION_NAME

MAX_SEQ_LENGTH = 2048

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = MODEL_PATH,
    max_seq_length = MAX_SEQ_LENGTH,
    load_in_4bit = True,
)
FastLanguageModel.for_inference(model)
tokenizer = get_chat_template(tokenizer, chat_template = "llama-3.2")

def chat():
    print(f"--- {VERSION_NAME} ---")
    
    while True:
        user_input = input("\n👤 USER: ")
        if user_input.lower() in ["exit", "clear", "quit"]: break

        # Fresh context every turn to prevent 'persona drift'
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]

        # 1. Capture the dictionary (IDs + Mask)
        inputs = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt = True,
            return_tensors = "pt",
            return_dict = True, 
        ).to("cuda")

        # 2. Unpack with ** to satisfy the model's requirements
        outputs = model.generate(
            **inputs,             
            max_new_tokens = 250,
            temperature = 0.0,    # Kill the 'idiot' persona by removing randomness
            do_sample = False,    # Forced Greedy Decoding
            repetition_penalty = 1.2,
            pad_token_id = tokenizer.eos_token_id
        )

        # 3. Slice the output to get only the new response
        input_length = inputs["input_ids"].shape[1]
        response = tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)

        # THE URL EXECUTIONER: If the model tries to show a link, we block it.
        '''
        if "http" in response or "redd.it" in response:
            final_response = (
                "TECHNICAL ERROR: Source data contains image artifacts. "
                "RE-ROUTING TO CORE LOGIC: MX is a reload-speed specialist. "
                "Arbalest is the preferred pairing for 'Last Shot' proc loops."
            )
        else:
        '''
        final_response = response.strip()

        # Log to Markdown with Metadata
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"""
---
### 🧪 Inference Test: {timestamp}
* **Model:** `{os.path.basename(MODEL_PATH)}`
* **Max Seq Length:** `{MAX_SEQ_LENGTH}`
* **Prompt Version:** `{VERSION_NAME}`
* **Query:** {user_input}
* **Response:** > {final_response}
"""  
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(log_entry)                    
        
        print(f"\n🤖 CODEX: {final_response}")

if __name__ == "__main__":
    chat()