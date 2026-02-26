import json
import re

input_file = './data/zombie_waves_master_codex_chatml_final.jsonl'
output_file = './data/zombie_waves_master_codex_refined.jsonl'

def refine_tone(text):
    # 1. Expanded "Chatty" filler and profanity list
    # Targets interjections, casual agreement, and informal fillers
    chatter_pattern = r'\b(fk|hmmm+|uhhh+|ummm+|wait wait|yea|yeah|yep|lol|haha|hehe|basically|actually|honestly|just|idk|asap|garbage|anyways?)\b'
    text = re.sub(chatter_pattern, '', text, flags=re.IGNORECASE)
    
    # 2. Remove Emojis and Discord placeholders
    text = re.sub(r'\|[a-z]+\|', '', text) # Targets |joy| style placeholders
    text = re.sub(r'[;:][-)]+', '', text)   # Targets simple emoticons like ;)
    
    # 3. Transform "I think/maybe/I guess" into authoritative statements
    hedging_map = {
        "I guess": "It appears",
        "maybe actually no": "Upon further analysis,",
        "Probably you can": "It is recommended to",
        "I'm not sure but": "Evidence suggests",
        "I believe that": "It is established that",
        "i cant": "it is difficult to determine"
    }
    for old, new in hedging_map.items():
        text = text.replace(old, new)

    # 4. Standardize Technical Shorthand (British English focused)
    # Ensuring 'Damage' and 'Attack' are used consistently
    shorthand_map = {
        "dmg": "damage",
        "atk": "attack",
        "hp": "HP",
        "lvl": "level",
        "eq": "equipment",
        "arba": "Arbalest",
        "pulv": "Pulverizer"
    }
    for old, new in shorthand_map.items():
        # Using regex to ensure we only replace whole words
        text = re.sub(rf'\b{old}\b', new, text, flags=re.IGNORECASE)

    # 5. Remove community-specific conversational markers
    community_markers = r'\b(hey everyone|you guys|thanks again|ingame|f2p)\b'
    text = re.sub(community_markers, '', text, flags=re.IGNORECASE)

    # Clean up whitespace and literal newlines
    text = text.replace('\\n', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

refined_count = 0

with open(input_file, 'r', encoding='utf-8') as f_in, \
     open(output_file, 'w', encoding='utf-8') as f_out:
    for line in f_in:
        data = json.loads(line)
        
        # We focus specifically on the assistant's role to maintain character
        for msg in data['messages']:
            if msg['role'] == 'assistant':
                original = msg['content']
                msg['content'] = refine_tone(original)
                if original != msg['content']:
                    refined_count += 1
        
        f_out.write(json.dumps(data) + '\n')

print(f"Refinement complete. {refined_count} entries have been polished for the AI Codex persona.")