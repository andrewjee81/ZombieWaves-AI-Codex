# 🧠 AI Training & Infrastructure Manifesto
**Project:** ZombieWaves AI Codex  
**Phase:** Supervised Fine-Tuning (SFT)  
**Status:** Environment Initialisation

This document outlines the technical strategy for fine-tuning a Large Language Model (LLM) on consumer-grade hardware. It chronicles the transition from raw data engineering to active model training.

---

## ✅ Hugging Face Cloud Integration
To ensure data redundancy and provide a professional "Source of Truth" for the portfolio, the refined dataset has been mirrored to the Hugging Face Hub.

- **Repository:** `[Your-Username]/zombiewaves-strategy-codex`
- **Visibility:** Private (Version Control)
- **Dataset Size:** 16,069 high-signal pairs
- **Format:** JSONL (Instruction-Response)

---

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

---

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
| **Model**           | Llama-3.2-3B-Instruct-bnb-4bit| Optimised 4-bit base for 4GB VRAM.                |
| **Max Seq Length**  | 2048                          | Balanced context window for strategy guides.      |
| **Rank (r)**        | 16                            | Learning capacity vs Memory tradeoff.             |
| **Batch Size**      | 1                             | Minimum VRAM overhead per step.                   |
| **Grad Accumulation**| 4                             | Simulates a larger batch size for stability.      |
| **Epochs**          | 1                             | Prevents over-fitting on 16k samples.             |
| **Grad Checkpoint** | True (Unsloth)                | Recomputes activations to save VRAM.              |
```

🧪 Evaluation Metrics
Results pending completion of the first training epoch. The model will be evaluated based on its ability to provide specific Zombie Waves strategy (e.g., weapon prioritisation and stage-specific boss tactics).