# 🧠 AI Training & Infrastructure Manifesto
**Project:** ZombieWaves AI Codex  
**Phase:** Supervised Fine-Tuning (SFT)  
**Status:** Environment Initialisation

This document outlines the technical strategy for fine-tuning a Large Language Model (LLM) on consumer-grade hardware. It chronicles the transition from raw data engineering to active model training.

---

## ✅ Hugging Face Cloud Integration
To ensure data redundancy and provide a professional "Source of Truth" for the portfolio, the refined dataset has been mirrored to the Hugging Face Hub.

- **Repository:** `andrewjee/zombiewaves-strategy-codex`
- **Visibility:** Private (Version Control)
- **Dataset Size:** 16,069 high-signal pairs
- **Format:** JSONL (Instruction-Response)


## 🖥️ Local Rig Configuration (NVIDIA GPU)
The training pipeline is architected to leverage local NVIDIA hardware via WSL2, ensuring zero cloud-compute costs and full data sovereignty.

### 🔧 Hardware Specifications
- **GPU:** NVIDIA GeForce RTX 3050 (Mobile/Laptop)
- **VRAM:** 4096 MiB (4GB GDDR6)
- **Driver Version:** 591.44
- **CUDA Version:** 13.1

### 🎯 Strategy: Small Language Model (SLM) Specialisation
Given the **4GB VRAM** constraint, the project pivots from Llama-3-8B to the **Llama-3.2-3B-Instruct** architecture. 
- **Rationale:** 3B models provide the optimal balance of reasoning capability and memory efficiency, fitting within the 4GB envelope when using Unsloth's 4-bit optimisations.
- **Optimisation:** QLoRA (Quantised Low-Rank Adaptation) will be utilised to reduce the memory footprint by ~70%.


## 🛠️ Environment Setup: `codex-train`
A dedicated Conda environment manages the specific dependency stack required for Unsloth and Xformers.

```bash
# Environment Creation
conda create --name codex-train python=3.10 -y
conda activate codex-train
```

# Core Dependency Stack
```bash
pip install torch torchvision torchaudio --index-url [https://download.pytorch.org/whl/cu121](https://download.pytorch.org/whl/cu121)
pip install "unsloth[colab-new] @ git+[https://github.com/unslothai/unsloth.git](https://github.com/unslothai/unsloth.git)"
pip install --no-deps "xformers<0.0.29" "trl<0.9.0" peft accelerate bitsandbytes
```

## 🚀 Training Hyperparameters (Low-VRAM Profile)
To prevent "Out of Memory" (OOM) errors on the RTX 3050, the following constraints are applied:

```Markdown
| Parameter           | Value                         | Logic                                             |
| :------------------ | :---------------------------- | :------------------------------------------------ |
| Model               | Llama-3.2-3B-Instruct-bnb-4bit| Optimised 4-bit base for 4GB VRAM.                |
| Max Seq Length      | 2048                          | Balanced context window for strategy guides.      |
| Rank (r)            | 16                            | Learning capacity vs Memory tradeoff.             |
| Batch Size          | 1                             | Minimum VRAM overhead per step.                   |
| Grad Accumulation   | 8                             | Simulates a larger batch size for stability.      |
| Epochs              | 1                             | Prevents over-fitting on 16k samples.             |
| Grad Checkpoint     | True (Unsloth)                | Recomputes activations to save VRAM.              |
```

🧪 Evaluation Metrics
Results pending completion of the first training epoch. The model will be evaluated based on its ability to provide specific Zombie Waves strategy (e.g., weapon prioritisation and stage-specific boss tactics).

## ⚖️ The v6.1 "Gold Truth" Decree: The Great Purge
**Status:** Enforced as of Feb 2026  
**Goal:** Shift from "Quantity" to "Mechanical Authority."

After auditing the v5 performance, it was clear that "Reddit Chatter" was causing the model to stutter and give "maybe" answers. v6.1 introduces a strict semantic sieve to ensure the Codex only learns **Veteran-Level Strategy.**

### 1. The v6.1 Audit Benchmark (Parallel Validation)
We no longer trust raw scrapes.
* **Method A: Heuristic Script ([_utils/auditor_python.py](_utils/auditor_python.py))**
  - **Logic:** Used keywords and regex for formatting and British English normalization.
  - **Result:** High speed, but lacked the "contextual brain" to see through social chatter.

* **Method B: AI Judge ([_utils/auditor_llama.py](_utils/auditor_llama.py))**
  - **Logic:** Llama-3.2-3B evaluated entries for strategic value and mechanical accuracy.
  - **Result:** Successfully identified 452 entries of "Extra Trash" that Method A missed.

**The Decree:** Based on this parallel test, the AI Judge is now the "Authority" for all future Codex data. While Method A remains useful for pre-cleaning, the AI's verdict is the final requirement for v6.1 inclusion.

### 2. Non-Negotiable Mechanical Denials
The following "Hallucinations" from previous versions are now strictly prohibited. If an entry suggests these, it is binned:
* **The EoH Conflict:** Eye of the Hurricane (EoH) **must not** be paired with Miniclip. It mandates Windborne/Dodge logic only.
* **The MX Loop:** Modified Xyclon (MX) **must** use the Miniclip/Reload loop. No exceptions.
* **Diamond Discipline:** The "27k Rule" for Aeroplane Chess is the only accepted economy strategy for F2P/Low-Spenders.

### 3. Authority Weighting (5:1 Ratio)
To ensure the model listens to the "Gold Truth" over the "Silver Scrapes," the training script (`merge_training_data_v2.py`) will repeat Core Gold files 5 times for every 1 time it reads a Reddit thread.