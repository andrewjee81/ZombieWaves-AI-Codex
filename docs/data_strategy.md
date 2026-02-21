## 📊 Data Strategy: Zombie Waves AI Codex
### 1. Vision & Narrative
The Zombie Waves AI Codex is a specialized expert system designed to provide high-fidelity strategy advice. To achieve a "teammate" feel rather than a "search engine" feel, the project transitioned from a static instruction format to a Conversational ChatML architecture.  

We utilize a multi-source data pipeline, integrating Discord community intelligence, Reddit strategy threads, and in-game mechanics to create a unified knowledge base.

### 2. The Great Pivot: Alpaca to ChatML
Initially, the project utilized the Alpaca Format (Instruction, Input, Output). However, we shifted to ChatML (System, User, Assistant) for the following strategic reasons:

- **Multi-Turn Logic:** ChatML allows the model to handle follow-up questions (e.g., "What about for Boreas?") by maintaining a conversational thread.

- **Persona Reinforcement:** By embedding the SYSTEM_PROMPT into every training example, we ensure the model maintains its identity as a focused strategy assistant.

- **Llama 3 Native Alignment:** Modern models like Llama 3 are pre-trained on conversational tokens. ChatML leverages this "native grammar" for more natural responses.

### 3. Data Processing Pipeline
A. Discord Intelligence
 - **Source:** Raw JSON exports from clean-discord.
 - **Processing:**
   - **Detox & Antispam:** Removed toxicity and bot commands using library flags.
   - **Conversational Grouping:** Logic treats the first message in a timestamp-grouped block as the user and subsequent replies as a single assistant block.
   - **Anonymization:** Strips Discord handles and IDs to preserve community privacy.

B. Reddit Strategy
 - **Source:** High-karma strategy threads (refined_training_data.jsonl).
 - **Processing:**
   - **Karma-Weighted Filtering:** Only top-voted comments were selected to ensure the "Assistant" provides "Meta" (optimal) advice.
   - **Markdown Normalization:** Removed Reddit-specific links and flattened excessive newlines to optimize token efficiency.

Legacy data preparation scripts (Alpaca-to-ChatML, Noise Filtering, and JSONL Merging) are archived in the _utils directory to maintain a clean production environment.


### 4. The Unified Guardrail (System Prompt)
Every training row is anchored by the following constant:

```Phyton
SYSTEM_PROMPT = (
    "You are the Zombie Waves AI Codex, an expert strategy assistant specializing in gear optimization, "
    "trait stacking logic, and high-efficiency build architecture. "
    "Your goal is to provide accurate, concise, and helpful gameplay advice for Zombie Waves. "
    "Stay in character and only discuss Zombie Waves content."
)
```

### 5. Data Architecture & Weighting
- **Gold Standard Repository:** Contains verified hand-built Hero Guides and the Veteran PDF Codex.
- **Community Pool:** Contains filtered Reddit and Discord data for conversational variety.
- **Weighting Logic:** During training set generation, the Gold Standard files are oversampled 5x. This ensures that even in a limited step count, the model prioritizes verified mechanics over community anecdotes.

### 6. Training Optimization: "The Long Burn"
- **Noise Reduction:** Implemented a threshold (10+ words) and keyword-matching to remove "platform noise" (e.g., Reddit upvotes, greetings).
- **Training Hyperparameters:**
  - Per Device Batch Size: 1
  - Gradient Accumulation Steps: 8
  - Effective Batch Size: 8 (1 × 8)
  - Max Steps: 1,200  
- **The Logic:** This "Long Burn" allows the model to deeply "soak" in ~9,600 high-density examples. It provides the best balance between learning complexity and hardware management for a 4GB VRAM card.

### 7. Future Maintenance: The Re-Pooling Plan
1. Add new patch data (e.g., a new S-Tier hero) to the Gold Repository.
2. Generate a new Augmented Training Set with the 5x weighting.
3. Retrain on the updated pool to prevent "Catastrophic Forgetting" and maintain a unified intelligence.

## Implementation Status

| Source | Status | Format | Count (Approx) |
| :--- | :--- | :--- | :--- |
| **Discord Intelligence** | ✅ **Processed** | ChatML | ~3,000 Samples |
| **Reddit Strategy** | ✅ **Processed** | ChatML |  ~16,069 Samples |
| **YouTube Transcripts** | ✅ **Processed** | ChatML | 11 Samples |
| **In-Game Codex (High Level)** | ✅ **Processed** | ChatML | 115 Samples |
| **PDF Strategy (High Level)** | ✅ **Processed** | ChatML | 45 Samples |

---
## 📑 Project Report: The v5 Technical Pivot
Date: 2026-02-21

Subject: Transition from High-Volume Data to "Veteran-Logic" Sanitisation

### 1. The Catalyst: Live Testing Failure  
During live-chat testing of the v4 model, significant hallucinations and contradictory logic were identified.

- **The Symptom:** The model suggested "Attack Speed" builds for Modified Xyclon (MX), which is mechanically suboptimal for the 2026 meta.

- **The Root Cause:** The model was "averaging" high-quality veteran advice with low-quality, outdated YouTube transcripts and legacy PDF guides that contained "Math Noise" and legacy weapon names (e.g., Zephyr, Voltstrike).

### 2. Discovered Vulnerabilities  
- **The YouTube Transcript Trap:** While transcripts provided "flavour," they introduced too much conversational filler and inconsistent terminology. The AI struggled to distinguish between a creator’s opinion and the game's "Gold Truth" mechanics.

- **Arithmetic Hallucinations:** Inclusion of explicit damage formulas (e.g., 1.6x + 30%) caused the AI to attempt manual math, which it often failed.

- **Entity Fragmentation:** Multiple names for the same items (e.g., Frost Meteor vs. Ice Cannon) split the model's understanding, leading to fragmented and weak strategy responses.

### 3. The v5 Correction (The "Cleansing" Results)  
To resolve these issues, the following Sanitisation Strategy was implemented for the v5 training set:

- **Removal of YouTube Data:** Deleted all raw transcripts to eliminate conversational noise and unverified "day-one" opinions.

- **PDF Strategy Refinement:** Stripped out all arithmetic formulas, replacing them with Mechanical Interaction Logic (e.g., "Multiplicative Elemental Scaling").

- **Gold Truth Anchoring:** The master_codex.jsonl was rebuilt around three non-negotiable veteran pillars:

- **The MX Reload Loop:** Strict adherence to the Miniclip/Reload meta.

- **Camp Infrastructure:** Correctly separating the Testworks Research Building from the Tower Mode.

- **Standardised Nomenclature:** Forcing the use of Boreas, Volt Gun, and Frost Meteor.

### 4. Expected Results for v5 Training  
By shifting the data weight from Quantity to Mechanical Accuracy, the v5 model is expected to:

  1. **Sound like a Veteran:** Provide high-density technical advice using British English.
  2. **Eliminate Contradictions:** Provide a single, coherent "Best-in-Slot" strategy for any given hero/weapon.
  3. **Reduce Hallucination:** By removing "Math Noise," the AI will describe how a build scales rather than guessing wrong damage numbers.