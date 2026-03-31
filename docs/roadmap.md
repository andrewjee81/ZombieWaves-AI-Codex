## 🛣️ Zombie Waves AI Codex: Strategic Roadmap (v8.1 Update)

### Phase 1: Heuristic Scripting (The Regex Era)
- **Method:** Utilised `_utils/legacy/auditor_python.py` focusing on keywords and formatting.
- **Pros:** Fast; zero VRAM footprint.
- **Status:** ✅ Completed (Tools archived in `_utils/legacy`).

### Phase 2: Local Semantic Judge (The 3B Era)
- **Method:** Employed a **Qwen 2.5 3B-Instruct** judge model on the local RTX 3050.
- **Environment:** Ubuntu 24.04.1 LTS via WSL2.
- **Constraint:** Initial 4GB VRAM limit restricted reasoning depth to a 1024-token context window.

### Phase 3: The TurboQuant+ Breakthrough (Current)
- **Method:** Migration to **TurboQuant+ Engine** with **QJL Error Correction**.
- **Strategy:** Implementation of 6x KV Cache compression based on **March 2026 Google Research**.
- **Key Changes:**
    - **Context Expansion:** Native support for **8192-token** sequences on 4GB VRAM.
    - **Local Independence:** Transitioned away from Cloud-Hybrid (Google Colab) dependencies by optimising local inference kernels.
    - **Gold Truth Verification:** Integration of **Veteran-led weighting** to resolve Discord/Reddit contradictions.

### Phase 4: The Multimodal Strategy Oracle (v8.2+)
- **Model Shift:** Transitioning to **Qwen 2.5 Omni (4-bit)** to enable visual-spatial reasoning.
- **Goal:** Allow the model to analyse **Hero/Gear screenshots** to provide tailored advice without manual stat entry.
- **Philosophy:** Focus remains on being a **Technical Strategy Guide**. This preserves the project's educational focus while ensuring 100% user-controlled execution (Non-Agentic).

---

## 🛠️ Technical Decisions & Constraints
- **The 4GB VRAM Ceiling:** Fixed at 4096 MiB. This necessitates the continued use of **TurboQuant+** and **Nightly PyTorch** builds.
- **Nomenclature Standardisation:** Strict enforcement of terms like "Boreas" and "MX Reload Loop" to prevent identity fragmentation.
- **Mechanical Denials:** Absolute rejection of "Mechanical Conflicts" (e.g., pairing Miniclip with Eye of the Hurricane).