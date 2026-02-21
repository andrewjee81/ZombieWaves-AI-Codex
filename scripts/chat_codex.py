import torch
from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template

# --- CONFIG ---
MODEL_PATH = "./final_codex_model_v4"

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = MODEL_PATH,
    max_seq_length = 2048,
    load_in_4bit = True,
)
FastLanguageModel.for_inference(model)
tokenizer = get_chat_template(tokenizer, chat_template = "llama-3.2")

SYSTEM_PROMPT = (
    "### ZOMBIE WAVES MASTER CODEX ###\n"
    "--- CORE ENGINE LAWS ---\n"
    "1. THE RELOAD LAW (MX): MX = Arbalest + Miniclip. Procs on reload. Mandatory pairing.\n"
    "2. THE HIT-RATE LAW (LIZZY): Lizzy = Volt Gun/Boreas. High Mag/Fire Rate. FORBIDDEN: Miniclip.\n"
    "3. THE ELEMENTAL LAW (SCORCHED EARTH): Fire Engine. Best with MOLLY or LIZZY. Focus on Fire Tree.\n"
    "4. WEAPON DATA: EoH = Wind/Frost (Endgame Wind). Volt Gun = Lightning.\n"
    "--- OUTPUT STYLE ---\n"
    "Technical British Veteran. Bullet points only. No first-person pronouns."
)

def fact_check(text):
    # Hard-correcting the model's common logic failures
    corrections = {
        "Voltpistol": "Volt Gun",
        "Modified Xyclon": "MX",
        "Mini-clip": "Miniclip",
        "victims": "zombies", # "Victims" is another weird translation quirk
    }
    for wrong, right in corrections.items():
        text = text.replace(wrong, right)
    return text

def chat():
    print("✅ CODEX v2.7: DETERMINISTIC MODE ACTIVE")
    
    while True:
        user_input = input("\n👤 USER: ")
        if user_input.lower() in ["exit", "clear"]: break

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
            max_new_tokens = 150,
            temperature = 0.0,    # Kill the 'idiot' persona by removing randomness
            do_sample = False,    # Forced Greedy Decoding
            repetition_penalty = 1.2,
            pad_token_id = tokenizer.eos_token_id
        )

        # 3. Slice the output to get only the new response
        input_length = inputs["input_ids"].shape[1]
        response = tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)

        # THE URL EXECUTIONER: If the model tries to show a link, we block it.
        if "http" in response or "redd.it" in response:
            final_response = (
                "TECHNICAL ERROR: Source data contains image artifacts. "
                "RE-ROUTING TO CORE LOGIC: MX is a reload-speed specialist. "
                "Arbalest is the preferred pairing for 'Last Shot' proc loops."
            )
        else:
            final_response = fact_check(response.strip())        
        
        print(f"\n🤖 CODEX: {final_response}")

if __name__ == "__main__":
    chat()