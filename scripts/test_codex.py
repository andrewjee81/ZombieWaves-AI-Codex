import os
os.environ["UNSLOTH_SKIP_TORCHVISION_CHECK"] = "1"
os.environ["UNSLOTH_SKIP_COMPILER"] = "1"

from unsloth import FastLanguageModel
import torch
from transformers import TextStreamer

# 1. Load the TRAINED model (Base + your LoRA adapters)
# We point to your output folder where the 60-step weights live
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "zombie_codex_outputs/checkpoint-60", # <--- Points to your specific run
    max_seq_length = 2048,
    load_in_4bit = True,
)

# 2. Switch to Inference Mode (Optimizes for speed/VRAM)
FastLanguageModel.for_inference(model)

# 3. Define the Prompt (Using your exact training format)
instruction = "What is the best ultimate for a stage with high physical resistance zombies?"
prompt = f"### Instruction:\n{instruction}\n\n### Response:\n"

# 4. Generate
inputs = tokenizer([prompt], return_tensors = "pt").to("cuda")
text_streamer = TextStreamer(tokenizer)

print("\n🤖 CODEX (60-STEP) RESPONSE:")
_ = model.generate(**inputs, streamer = text_streamer, max_new_tokens = 128)