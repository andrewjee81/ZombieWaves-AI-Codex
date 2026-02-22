"""
================================================================
ZOMBIE WAVES AI CODEX: TRAINING SUITE
================================================================
Module: Strategic Meta Injection

PURPOSE:
This script performs a targeted fine-tuning (SFT) 'patch' on the latest
version adapter weights.
"""
from unsloth import FastLanguageModel
import torch
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset
import os
from config import EXT_MODEL_DIR, MODEL_PATH, LOCAL_DATA_DIR

# --- SETTINGS & CONSTANTS (PEP 8 UPPER_CASE) ---
PATCHED_MODEL_PATH = os.path.join(EXT_MODEL_DIR, "final_codex_model_v6")
DATA_FILE_PATH = os.path.join(LOCAL_DATA_DIR, "logic_patch.jsonl")

LEARNING_RATE = 6e-6 # Low and slow
MAX_STEPS = 120      # Stop before the collapse
MAX_SEQ_LENGTH = 2048

# 1. Load the existing model (building on top of v5)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = MODEL_PATH, 
    max_seq_length = MAX_SEQ_LENGTH,
    load_in_4bit = True,
)

# 2. Load the 'Gold Truth' dataset
dataset = load_dataset("json", data_files=DATA_FILE_PATH, split="train")

# 3. Formatting function
def formatting_prompts_func(examples):
    instructions = examples["instruction"]
    contexts     = examples["context"]
    outputs      = examples["response"]
    texts = []
    for instruction, context, output in zip(instructions, contexts, outputs):
        # Standard Llama-3.2 Chat Format
        text = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nTechnical Strategy Engine. Context: {context}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{instruction}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n{output}<|eot_id|>"
        texts.append(text)
    return { "text" : texts, }

dataset = dataset.map(formatting_prompts_func, batched = True,)

# 4. Train with a focus on 'Injecting' 2026 Meta (Gale Shinobi / Robots)
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = MAX_SEQ_LENGTH,
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 5,
        max_steps = MAX_STEPS,
        learning_rate = LEARNING_RATE,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.5, # Keeps the model's 'brain' flexible
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
    ),
)

trainer_stats = trainer.train()

# 5. Save the Patched Model
model.save_pretrained(PATCHED_MODEL_PATH)
tokenizer.save_pretrained(PATCHED_MODEL_PATH)

print(f"v6 Patch Complete. Model saved to: {PATCHED_MODEL_PATH}")