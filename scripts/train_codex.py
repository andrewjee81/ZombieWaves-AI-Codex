'''
Module: train_codex.py
Project: ZombieWaves-AI-Codex
Description:
    Processes raw Reddit snapshots to remove PII (Personally Identifiable Information).
    Filters out 'deleted' or 'removed' content and applies a blacklist of post IDs
    to respect user 'Right to Erasure' requests.
Key Objective: Anonymise data while preserving strategic game context.



4-bit Quantization: Shrinks the model so it occupies roughly 3.5GB of your 4GB.

8-bit Optimizer: Standard optimizers take up a lot of VRAM; the 8-bit version is much "leaner."

Gradient Accumulation: Instead of trying to process 4 examples at once (which would crash your card), it processes 1 example four times and then updates, giving you the quality of a larger batch without the VRAM cost.
'''

import os
os.environ["UNSLOTH_SKIP_TORCHVISION_CHECK"] = "1"
os.environ["UNSLOTH_SKIP_COMPILER"] = "1"

from unsloth import FastLanguageModel
import torch
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset
from unsloth.chat_templates import get_chat_template

# 1. Load Model with 4-bit Quantization (Optimised for 4GB 3050)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Llama-3.2-3B-Instruct-bnb-4bit",
    max_seq_length = 2048,
    load_in_4bit = True,
)

# 2. Add LoRA Adapters (The codex "Brain" with minimal footprint for 4GB)
model = FastLanguageModel.get_peft_model(
    model,
    r = 16, # Increased to 16 for better intelligence, still fits in 4GB
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_alpha = 32,
    lora_dropout = 0,
    bias = "none",
)

# 3. Load Dataset
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)
data_path = os.path.join(root_dir, "data", "training_master_v5_weighted.jsonl")

# Load the dataset
dataset = load_dataset("json", data_files=data_path, split="train")

print(f"✅ Loading data from: {data_path}")

# 4. Standardise ChatML to Llama-3 Template
tokenizer = get_chat_template(
    tokenizer,
    chat_template = "llama-3", # This maps your {"messages": ...} to the model's brain
    mapping = {"role" : "role", "content" : "content", "user" : "user", "assistant" : "assistant"},
)

def formatting_prompts_func(examples):
    convos = examples["messages"]
    texts = [tokenizer.apply_chat_template(convo, tokenize = False, add_generation_prompt = False) for convo in convos]
    return { "text" : texts, }

dataset = dataset.map(formatting_prompts_func, batched = True)

# 5. Path Setup
external_drive_path = "/mnt/d/Project Codex/ZombieWaves-AI-Codex-Train"
final_model_path = os.path.join(external_drive_path, "final_codex_model_v5")

if not os.path.exists(external_drive_path):
    os.makedirs(external_drive_path)

# 6. The "3050 Stable" Config for Low VRAM
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = 512,
    args = TrainingArguments(
        output_dir = external_drive_path,
        per_device_train_batch_size = 1,
        gradient_accumulation_steps = 8, 
        warmup_steps = 10,       # Slightly more warmup for a longer run
        max_steps = 4000,        # The "Full Burn" for 19k examples
        learning_rate = 2e-5,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit", 
        weight_decay = 0.01,
        save_steps = 300,        # Save every 300 steps as a safety net
        save_total_limit = 2,    # Keeps only the 2 most recent saves (saves disk space)
    ),
)

print("\n🚀 ENGINE READY. Training ZombieWaves-AI-Codex V5 with weighted codex...")
trainer.train()

print(f"✅ Training Complete. Saving Master Codex...")
model.save_pretrained(final_model_path)
tokenizer.save_pretrained(final_model_path)

# Optional: Save as GGUF for mobile/local app use later?
# model.save_pretrained_gguf(final_model_path, tokenizer, quantization_method = "q4_k_m")

print(f"✨ Master Codex v2 ready at: {final_model_path}")