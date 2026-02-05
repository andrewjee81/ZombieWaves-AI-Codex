import pandas as pd
import re
from datasets import load_dataset

def de_reddit_text(text):
    if not isinstance(text, str): return text
    
    # 1. Remove First-Person "Fluff" (I think, In my opinion, etc.)
    fluff_patterns = [
        r"(?i)\b(i think|in my opinion|to me|for me|personally|i believe)\b,?\s*",
        r"(?i)\b(i'm not sure if|i am not sure if|i don't know if)\b,?\s*",
        r"(?i)\b(i've found that|i have found that|i noticed that)\b,?\s*",
        r"(?i)\b(hope this helps|good luck|just my two cents|edit:)\b.*"
    ]
    for pattern in fluff_patterns:
        text = re.sub(pattern, "", text)

    # 2. Convert First-Person to Objective (I use -> Use, I like -> Recommend)
    replacements = {
        r"(?i)\bi use\b": "Use",
        r"(?i)\bi recommend\b": "Recommended strategy:",
        r"(?i)\bi like using\b": "Effective strategy:",
        r"(?i)\bit saved me\b": "is effective",
    }
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)

    # 3. Clean up leading punctuation/whitespace left by removals
    text = text.strip().capitalize()
    text = re.sub(r"^[,\.\s]+", "", text)
    
    return text

# --- EXECUTION ---
print("📥 Loading original dataset...")
dataset = load_dataset("andrewjee/zombiewaves-strategy-codex", split="train")
df = pd.DataFrame(dataset)

print("🧹 Scrubbing Reddit personality...")
# Identify your columns (e.g., 'instruction' and 'output')
output_col = next((c for c in ["output", "response", "completion", "answer", "strategy"] if c in df.columns), "output")

df[output_col] = df[output_col].apply(de_reddit_text)

# 4. Save locally for training
clean_path = "data/zombiewaves_codex_cleaned.jsonl"
df.to_json(clean_path, orient="records", lines=True)

print(f"✅ Cleaned {len(df)} rows. Saved to: {clean_path}")
print("\n--- SAMPLE COMPARISON ---")
print(f"Original: I think the 3rd stage is best for me.")
print(f"Cleaned:  {de_reddit_text('I think the 3rd stage is best for me.')}")