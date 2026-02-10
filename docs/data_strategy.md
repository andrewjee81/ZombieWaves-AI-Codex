## 📊 Data Strategy: Zombie Waves AI Codex
### 1. Vision & Narrative
The Zombie Waves AI Codex is a specialized expert system designed to provide high-fidelity strategy advice. To achieve a "teammate" feel rather than a "search engine" feel, the project transitioned from a static instruction format to a Conversational ChatML architecture.  

We utilize a multi-source data pipeline, integrating Discord community intelligence, Reddit strategy threads, and in-game mechanics to create a unified knowledge base.

### 2. The Great Pivot: Alpaca to ChatML
Initially, the project utilized the Alpaca Format (Instruction, Input, Output). However, we shifted to ChatML (System, User, Assistant) for the following strategic reasons:

Multi-Turn Logic: ChatML allows the model to handle follow-up questions (e.g., "What about for Boreas?") by maintaining a conversational thread.

Persona Reinforcement: By embedding the SYSTEM_PROMPT into every training example, we ensure the model maintains its identity as a focused strategy assistant.

Llama 3 Native Alignment: Modern models like Llama 3 are pre-trained on conversational tokens. ChatML leverages this "native grammar" for more natural responses.

### 3. Data Processing Pipeline
A. Discord Intelligence (scripts/discord_to_chatml.py)
 - **Source:** Raw JSON exports from clean-discord.
 - **Processing:**
   - **Detox & Antispam:** Removed toxicity and bot commands using library flags.
   - **Conversational Grouping:** Logic treats the first message in a timestamp-grouped block as the user and subsequent replies as a single assistant block.
   - **Anonymization:** Strips Discord handles and IDs to preserve community privacy.

B. Reddit Strategy (scripts/reddit_to_chatml.py)
 - **Source:** High-karma strategy threads (refined_training_data.jsonl).
 - **Processing:**
   - **Karma-Weighted Filtering:** Only top-voted comments were selected to ensure the "Assistant" provides "Meta" (optimal) advice.
   - **Markdown Normalization:** Removed Reddit-specific links and flattened excessive newlines to optimize token efficiency.


### 4. The Unified Guardrail (System Prompt)
Every training row is anchored by the following constant:

```Phyton
SYSTEM_PROMPT = (
    "You are the Zombie Waves AI Codex, an expert strategy assistant. "
    "Your goal is to provide accurate, concise, and helpful gameplay advice "
    "for Zombie Waves. Stay in character and only discuss Zombie Waves content."
)
```

### 5. Implementation Status

| Source | Status | Format | Count (Approx) |
| :--- | :--- | :--- | :--- |
| **Discord Intelligence** | ✅ **Processed** | ChatML | ~3,000 Blocks |
| **Reddit Strategy** | ✅ **Processed** | ChatML | 16,069 Pairs |
| **YouTube Transcripts** | ⏳ **In Progress** | ChatML | *Pending Synth* |
| **In-Game Codex** | 📅 **Backlog** | ChatML | *Data Extraction* |