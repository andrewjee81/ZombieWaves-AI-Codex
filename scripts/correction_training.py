from unsloth import FastLanguageModel
import torch
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset

# 1. Load the existing model (it already has LoRA)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "./final_codex_model_v3", 
    max_seq_length = 2048,
    load_in_4bit = True,
)

# --- REMOVED get_peft_model call here because it's already a PEFT model ---

# 2. Load the 'Gold Truth' dataset
dataset = load_dataset("json", data_files="./data/gold_truth.jsonl", split="train")

# 3. Formatting function (Critical for Llama-3.2 logic)
def formatting_prompts_func(examples):
    instructions = examples["instruction"]
    contexts     = examples["context"]
    outputs      = examples["response"]
    texts = []
    for instruction, context, output in zip(instructions, contexts, outputs):
        # Using the standard chat format so it learns the 'tone' correctly
        text = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nTechnical Strategy Engine. Context: {context}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{instruction}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n{output}<|eot_id|>"
        texts.append(text)
    return { "text" : texts, }

dataset = dataset.map(formatting_prompts_func, batched = True,)

# 4. Train with a focus on 'unlearning' the hallucinations
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = 2048,
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        max_steps = 40,  # 40 steps is plenty for a 'wash'
        learning_rate = 5e-5, # Lower LR so we don't break the model, just steer it
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        output_dir = "outputs_wash",
    ),
)
trainer.train()

# 5. Save as v3
model.save_pretrained("final_codex_model_v4")
tokenizer.save_pretrained("final_codex_model_v4")