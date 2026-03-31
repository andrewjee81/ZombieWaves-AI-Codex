# 🧠 AI Training & Infrastructure Manifesto (v8.1 Update)
**Project:** Zombie Waves AI Codex  
**Status:** High-Efficiency Inference Validation (TurboQuant+)

---

## 🖥️ Local Rig Configuration (NVIDIA GPU)
The training and inference pipeline is architected to leverage local NVIDIA hardware via WSL2, ensuring zero cloud-compute costs and full data sovereignty.

### 🔧 Hardware Specifications
- **GPU:** NVIDIA GeForce RTX 3050 (Mobile/Laptop)
- **VRAM:** 4096 MiB (4GB GDDR6)
- **Driver Version:** 591.44 (Nightly Bridge)
- **CUDA Version:** 12.x / 13.1 (Experimental)

### 🎯 Strategy: Small Language Model (SLM) Specialisation
Given the **4GB VRAM** constraint, the project utilizes the **Qwen 2.5 3B-Instruct** architecture. 

- **Rationale:** While Llama-3.2 is robust, **Qwen 2.5** provides superior compatibility with the **TurboQuant+** engine. This allows for **6x KV Cache compression**, enabling a 3B model to maintain a **8192-token context window** on hardware that typically maxes out at 1024 tokens.
- **Accuracy:** Qwen 2.5 3B retains "Gold Truth" reasoning even under heavy quantization, making it the ideal "Auditor" for the 226-entry Codex dataset.

### ⚖️ The Auditor Evolution
* **Method A: Heuristic Script ([legacy/auditor_python.py](legacy/auditor_python.py))**
  - **Logic:** Keywords/Regex for formatting. Archived as a pre-cleaning baseline.
* **Method B: Semantic Turbo-Judge (Current)**
  - **Logic:** Qwen 2.5 3B with **QJL Error Correction**.
  - **Result:** Capable of scanning entire Reddit threads to identify mechanical contradictions (e.g., the "Miniclip on EoH" error) that simple scripts miss.

### 2. Non-Negotiable Mechanical Denials
The following "Hallucinations" are strictly prohibited. If an entry suggests these, it is binned:
* **The EoH Conflict:** Eye of the Hurricane (EoH) **must not** be paired with Miniclip. It mandates Windborne/Dodge logic only.
* **The MX Loop:** Modified Xyclon (MX) **must** use the Miniclip/Reload loop. No exceptions.
* **Diamond Discipline:** The "27k Rule" for Aeroplane Chess is the only accepted economy strategy for F2P players.

### 3. Authority Weighting (5:1 Ratio)
To ensure the model listens to the **"Gold Truth"** over the "Silver Scrap," we apply the following multipliers:
- **Official Codex/Veteran Verified:** 5x Weight.
- **General Reddit/Discord Sentiment:** 1x Weight.