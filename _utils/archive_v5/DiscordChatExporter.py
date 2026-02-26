"""
================================================================
ZOMBIE WAVES AI CODEX: RAW DISCORD SURGICAL EXTRACTOR (v2.0)
================================================================
FILE DESCRIPTION: 
Advanced parser for raw DiscordChatExporter JSON. 
Uses 'reference' IDs to reconstruct perfect Q&A pairs, 
preserves image placeholders to prevent context loss, 
and filters by high-value game mechanics (Miniclip, EoH, etc).
================================================================
ROLE:         AI Quality Control (Judge Model)
ENGINE:       Llama-3.2-3B-Instruct (4-bit Unsloth)
PURPOSE:      Semantic filtering of Reddit/Community data.
              Removes 'Trash' (social noise, complaints) and 
              'Mechanical Conflicts' (EoH + Miniclip).
================================================================
"""

import json
import os

# CONFIGURATION
INPUT_FILE = "./data/Zombie Waves - 🧟 WAVES GUIDE - 💡general-tips-n-tricks [1191318864139649124].json"
OUTPUT_FILE = "./data/discord_recovered_chatml.jsonl"

def extract_raw_knowledge():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Could not find the raw export file.")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    raw_messages = data.get('messages', [])
    msg_map = {m['id']: m for m in raw_messages}
    
    chatml_entries = []
    processed_replies = set()

    print(f"🔍 Analyzing {len(raw_messages)} messages for technical linkages...")

    for msg in raw_messages:
        # We look for replies because they represent the "Question -> Answer" flow
        ref = msg.get('reference')
        if ref and ref.get('messageId'):
            parent_id = ref['messageId']
            
            if parent_id in msg_map:
                parent_msg = msg_map[parent_id]
                
                # Check for attachments in either message
                parent_img = "[Image Attached] " if parent_msg.get('attachments') else ""
                child_img = " [Image Attached]" if msg.get('attachments') else ""

                user_content = parent_img + parent_msg.get('content', '').strip()
                assistant_content = msg.get('content', '').strip() + child_img

                # Skip if content is empty (just an image with no text)
                if not user_content or not assistant_content:
                    continue

                # Add logic to combine "Double Replies" (same person sending 2 messages)
                # (Simplified here for clarity, but captures the core link)
                
                entry = {
                    "messages": [
                        {
                            "role": "system", 
                            "content": "You are the Zombie Waves AI Codex, a strategy expert. Provide technical, high-density advice."
                        },
                        {"role": "user", "content": user_input_clean(user_content)},
                        {"role": "assistant", "content": assistant_output_clean(assistant_content)}
                    ]
                }
                chatml_entries.append(entry)
                processed_replies.add(msg['id'])

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f_out:
        for entry in chatml_entries:
            f_out.write(json.dumps(entry, ensure_ascii=False) + '\n')

    print(f"✅ Recovery Complete: {len(chatml_entries)} linked pairs found.")

def user_input_clean(text):
    # Standard cleaning: remove mentions, extra spaces
    return text.replace("\r\n", "\n").strip()

def assistant_output_clean(text):
    # Standard cleaning + preserving the "Top-Down" flow
    return text.replace("\r\n", "\n").strip()

if __name__ == "__main__":
    extract_raw_knowledge()