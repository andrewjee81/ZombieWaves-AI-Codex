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
# Updated Prompt with a System Persona
# System prompt to stop the "Penguin is a Hero" hallucination
system_prompt = """You are the ZombieWaves Strategy Codex. 
1. Always distinguish between Heroes (like MX) and Robots (like Penguin). 
2. Use specific trait names like 'Miniclip' and 'Entrenched'. 
3. Focus on 'No-Reload' synergies."""

instruction = "Which weapon should be paired with MX—Arbalest, Voltgun, or Pulse Laser Canon—and what is the best Robot to accompany them?"

# Build the Alpaca-style prompt with System instruction
prompt = f"### System:\n{system_prompt}\n\n### Instruction:\n{instruction}\n\n### Response:\n"


# 3. Generate the response
inputs = tokenizer([prompt], return_tensors = "pt").to("cuda")
outputs = model.generate(
    **inputs, 
    max_new_tokens = 128, 
    use_cache = True,
    temperature = 0.7,         # Adds a bit of "creativity" so it doesn't pick the same word
    top_p = 0.9,               # Nucleus sampling: filters out the "junk" low-probability words
    repetition_penalty = 1.2,  # THE CURE: Physically punishes the model for repeating words
    do_sample = True           # Enables the temperature/top_p settings
)
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