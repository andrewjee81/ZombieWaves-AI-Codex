import pandas as pd
import json

# 1. Configuration
SYSTEM_PROMPT = (
    "You are the Zombie Waves AI Codex, an expert strategy assistant. "
    "Your goal is to provide accurate, concise, and helpful gameplay advice "
    "for Zombie Waves. Stay in character and only discuss Zombie Waves content."
)

# 2. Official Localization Mapping
glossary = {
    "Frost Penguin": "Penguin",
    "Ullr": "Ullr Hatchling",
    "Calamity": "Calamity's Edge",
    "Gingerbread": "Gingerbread Man",
    "Bunny": "Bunny Band",
    "Snorf": "Snorf (Rocket Bat)",
    "Voltgun": "Voltstrike",
    "Eye of Hurricane": "Eye of the Hurricane"
}

def clean_text(text):
    if pd.isna(text): return ""
    for wrong, right in glossary.items():
        text = text.replace(wrong, right)
    return text

# 3. Processing Logic
def convert_to_jsonl(csv_path, output_path):
    df = pd.read_csv(csv_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            hero = row['Hero']
            traits = clean_text(row['Traits / Key Abilities'])
            weapon = clean_text(row['Best Weapon'])
            robots = clean_text(row['Robot Pairing'])
            style = row['Gameplay Style']
            
            # Construct a dense, expert-level response
            user_query = f"How should I build {hero} and what is the optimal playstyle?"
            assistant_response = (
                f"{hero} is a {row['Tier']}-tier hero best used for {row['Best Use']}. "
                f"Core Traits: {traits}. Optimal Loadout: Pair with {weapon} and robots {robots}. "
                f"Strategy: This is a {style} build. Focus on maximizing these specific synergies "
                f"to push high-level waves."
            )
            
            entry = {
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_query},
                    {"role": "assistant", "content": assistant_response}
                ]
            }
            f.write(json.dumps(entry) + '\n')

# Execute
convert_to_jsonl('/mnt/c/inetpub/wwwroot/GitHub/ZombieWaves-AI-Codex/data/Zombie waves - heroes.csv', '/mnt/c/inetpub/wwwroot/GitHub/ZombieWaves-AI-Codex/data/master_hero_data.jsonl')
print("Standardized Hero JSONL created successfully.")