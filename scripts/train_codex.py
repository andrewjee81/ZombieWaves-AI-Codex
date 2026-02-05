import os
os.environ["UNSLOTH_SKIP_TORCHVISION_CHECK"] = "1"
os.environ["UNSLOTH_SKIP_COMPILER"] = "1"

from unsloth import FastLanguageModel
import torch
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset

# 1. Load Model (Optimised for 4GB)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Llama-3.2-3B-Instruct-bnb-4bit",
    max_seq_length = 2048,
    load_in_4bit = True,
)

# 2. Add LoRA Adapters (Minimal footprint)
model = FastLanguageModel.get_peft_model(
    model,
    r = 8, 
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_alpha = 16,
    lora_dropout = 0,
    bias = "none",
)

# 3. Load Dataset
# dataset = load_dataset("andrewjee/zombiewaves-strategy-codex", split = "train")
dataset = load_dataset("json", data_files="data/zombiewaves_codex_cleaned.jsonl", split="train")

# DEBUG: See what the columns are actually called
print(f"DEBUG: Your dataset columns are: {dataset.column_names}")

def format_prompts(examples):
    # Determine the correct column names (trying common variations)
    # This checks for 'instruction' or 'prompt' or 'input'
    input_col = next((c for c in ["instruction", "prompt", "input", "question"] if c in examples), None)
    # This checks for 'output' or 'response' or 'completion' or 'answer'
    output_col = next((c for c in ["output", "response", "completion", "answer", "strategy"] if c in examples), None)

    if not input_col or not output_col:
        raise ValueError(f"Could not find matching columns. Columns available: {list(examples.keys())}")

    instructions = examples[input_col]
    outputs      = examples[output_col]
    
    texts = []
    for instruction, output in zip(instructions, outputs):
        # Formatting for Llama-3-style instruction following
        text = f"### Instruction:\n{instruction}\n\n### Response:\n{output}"
        texts.append(text)
    return { "text" : texts, }

# 4. Apply the mapping
dataset = dataset.map(format_prompts, batched=True)

external_drive_path = "/mnt/d/Project Codex/ZombieWaves-AI-Codex-Train"
final_model_path = os.path.join(external_drive_path, "final_codex_model")

# Ensure the folder exists
import os
if not os.path.exists(external_drive_path):
    os.makedirs(external_drive_path)

# 5. The "3050 Stable" Config
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = 2048,
    args = TrainingArguments(
        output_dir = external_drive_path, # Saves checkpoints here
        per_device_train_batch_size = 1,
        gradient_accumulation_steps = 16,
        warmup_steps = 5,
        max_steps = 1000, # Increased for a "Full Burn"
        learning_rate = 2e-4,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.01,
        save_total_limit = 3, # Keep only the 3 latest checkpoints to save HDD space
    ),
)

print("\n🚀 ENGINE READY. Starting ZombieWaves-AI-Codex Training...")
trainer.train()

# This saves a clean version without optimizer states (smaller file size)
model.save_pretrained(final_model_path)
tokenizer.save_pretrained(final_model_path)
print(f"✅ Training Complete. Final model saved to: {final_model_path}")