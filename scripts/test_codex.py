import os
from datetime import datetime
from unsloth import FastLanguageModel
import torch

# --- CONFIGURATION ---
model_path = "/mnt/d/Project Codex/ZombieWaves-AI-Codex-Train/final_codex_model"
log_file_path = "/mnt/c/inetpub/wwwroot/GitHub/ZombieWaves-AI-Codex/docs/training_log.md"

# 1. Load the model and tokenizer
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = model_path,
    max_seq_length = 2048,
    load_in_4bit = True,
)
FastLanguageModel.for_inference(model)

# 2. Define the test case
instruction = "Which weapon should be paired with Modified Xyclon (MX) between the Arbalest, Voltgun, and Pulse Laser Canon, and what are the essential traits required to trigger his infinite ammo state?"
prompt = f"### Instruction:\n{instruction}\n\n### Response:\n"

# 3. Generate the response
inputs = tokenizer([prompt], return_tensors = "pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens = 128, use_cache = True)
response = tokenizer.batch_decode(outputs)

# Clean up the output to get only the response text
final_response = response[0].split("### Response:\n")[-1].replace(tokenizer.eos_token, "").strip()

# 4. Log to Markdown
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_entry = f"""
---
### 🧪 Inference Test: {timestamp}
* **Model Version:** {os.path.basename(model_path)}
* **Instruction:** {instruction}
* **Response:** > {final_response}

"""

with open(log_file_path, "a", encoding="utf-8") as f:
    f.write(log_entry)

print(f"✅ Inference complete. Response logged to {log_file_path}")
print(f"\nModel Output:\n{final_response}")