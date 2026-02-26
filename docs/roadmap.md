## 🛣️ Zombie Waves AI Codex: Data Quality Roadmap (2026-02-25)
1. Evolution of the Auditor Strategy  
This section chronicles the transition from simple filtering to intelligence-based logic verification to overcome hardware constraints.

Phase 1: Heuristic Scripting (The Regex Era)  
- **Method:** Utilised _utils/auditor_python.py focusing on keywords and formatting.

- **Pros:** Fast; zero VRAM footprint.

- **Cons:** High noise floor; unable to identify mechanical contradictions like the "Miniclip on EoH" conflict.

Phase 2: Local Semantic Judge (The 3B Era)
- **Method:** Employed a Llama-3.2-3B-Instruct judge model on the local RTX 3050.

- **Environment:** Ubuntu 24.04.1 LTS via WSL2.

- **Cons:** 4GB VRAM limit restricted the model's reasoning depth; prone to "hallucinated" advice when processing high-volume Reddit data.

Phase 3: Cloud-Hybrid Logic
- **Method:** Qwen2.5-7B-Instruct (4-bit Unsloth) hosted on Google Colab.

- **Strategy:** Direct-Inference & Checkpointing.

- **Key Changes:**
    - **Logic over Language:** Removed British English constraints during the audit to prevent instructional noise and speed up processing of American-sourced Reddit data.
    - **Assistant Pre-filling:** Used the `Assistant: [` prompt hack to bypass "Chain of Thought" reasoning, increasing throughput from 1 sample/sec to ~4 samples/sec.
    - **Distributed Processing:** Utilised three separate Google Colab accounts to bypass free-tier compute limits, managed via a line-count checkpointing script.
    - **Nomenclature Alignment:** Focused purely on enforcing mechanical truths (e.g., MX Reload Loop and EoH Dodge Logic) as defined in the `master_codex.jsonl`.

- **Goal:** To produce verified_reddit_gold.jsonl, a mechanically perfect dataset that acts as a "Silver-to-Gold" bridge for final 3B training.

---

## 🛠️ Technical Decisions & Constraints
- **The 3050 VRAM Ceiling:** Fixed at 4096 MiB. This necessitated moving the "heavy thinking" (the audit) to the cloud so the local GPU remains dedicated to the final Supervised Fine-Tuning (SFT).

- **Nomenclature Standardisation:** Strict enforcement of terms like "Boreas" and "MX Reload Loop" to prevent identity fragmentation in the model's weights.

- **Mechanical Denials:** Absolute rejection of any advice suggesting Miniclip for Eye of the Hurricane (EoH).