# 🧟 Project Codex: Zombie Waves AI Strategy Engine
> An Advanced RAG (Retrieval-Augmented Generation) & Fine-Tuning Engine for Zombie Waves Game Strategy.

[![Licence: MIT](https://img.shields.io/badge/Licence-MIT-yellow.svg)](https://opensource.org/licences/MIT)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/)
[![WSL2-Ubuntu](https://img.shields.io/badge/OS-Ubuntu_24.04_LTS-orange.svg)](https://ubuntu.com/)
[![GPU-Acceleration](https://img.shields.io/badge/Hardware-NVIDIA_RTX-green.svg)](https://developer.nvidia.com/cuda-zone)
![Status: Work in Progress](https://img.shields.io/badge/status-wip-orange)

**Project Codex** is a non-commercial, educational research project designed to build a high-fidelity "Expert AI" for the mobile game Zombie Waves. By leveraging large-scale community datasets from public research archives and executing local fine-tuning on a dedicated NVIDIA-powered workstation, this project explores the intersection of community-driven game theory and Large Language Model (LLM) optimisation.

---

## 🎯 Overview
**ZombieWaves AI-Codex** is an end-to-end data pipeline and AI engine designed to synthesise high-level game meta-strategies. The "Codex" mines thousands of community discussions and expert guides to provide optimised build paths, hero synergies (e.g., MX Hero), and stage-specific tactical advice.

The primary objective is to ingest large volumes of unstructured community data ranging from synergies and hero builds to game exploits—and transform it into a structured, high-signal knowledge base. This refined data serves as the foundation for fine-tuning a specialised LLM, turning "chatter" into actionable strategic intelligence.


## 📊 System Architecture & Data Flow (Updated 2026-02-10)
```mermaid
graph TD
    %% Source Layer
    subgraph Sources [Raw Data Sources]
        D_Raw[Discord JSON<br/>39k Messages]
        R_Raw[Reddit JSON<br/>Strategy Threads]
        Y_Raw[YouTube Transcripts<br/>Video Content]
        G_Raw[In-Game Codex<br/>Official Stats]
    end

    %% Processing Layer
    subgraph Processing [Cleaning & Refinement]
        D_Clean[clean-discord.py<br/>Detox & Antispam]
        R_Refine[refiner.py<br/>Karma-Weighted Filter]
        Y_Chunk[Chunker Script<br/>Synth & Summarize]
    end

    %% Transformation Layer
    subgraph Transformation [Conversational Alignment]
        System_Prompt{{System Prompt Guardrail}}
        ChatML_Conv[ChatML Transformation<br/>Role: System/User/Assistant]
    end

    %% Data Preparation Layer
    subgraph Data_Prep [Data Preparation]
        Master_File[(master_codex_data.jsonl)]
        Tokenize[Tokenization]
    end

    %% GPU Optimization Layer
    subgraph GPU_Optimization [4GB VRAM Rig]
        Loader{Unsloth Loader}
        NF4[4-bit NF4 Quant]
        GRAD[Gradient Checkpointing]
        RANK[LoRA Rank: 8]
        MSL[Max Seq Length: 1024]
    end

    %% Final Output
    subgraph Result [Final Codex]
        Final_Weights[[Fine-Tuned Weights]]
    end

    %% Main Flow Connections
    D_Raw --> D_Clean
    R_Raw --> R_Refine
    Y_Raw --> Y_Chunk
    G_Raw --> ChatML_Conv

    D_Clean --> ChatML_Conv
    R_Refine --> ChatML_Conv
    Y_Chunk --> ChatML_Conv

    System_Prompt --> ChatML_Conv
    ChatML_Conv --> Master_File
    Master_File --> Tokenize
    Tokenize --> Loader

    %% Optimization Connections
    Loader --> NF4
    Loader --> GRAD
    Loader --> RANK
    Loader --> MSL

    %% Finalizing
    NF4 & GRAD & RANK & MSL --> Final_Weights
```


## 🏗️ Architecture & Tech Stack
This project is built on a high-performance local workstation (ASUS RTX Rig) to ensure data privacy and rapid iteration.

- **Infrastructure:** Ubuntu 24.04 LTS via WSL2.
- **Data Engine:** Custom extraction pipeline using `zstd` and `grep` to process multi-gigabyte Reddit data dumps (Pushshift/Academic Torrents).
- **AI/ML:** - **Framework:** PyTorch with CUDA 12.1 hardware acceleration.
- **Environment:** Miniconda for isolated dependency management.
- **Models:** (Planned) Llama 3 fine-tuned on specialised game datasets.

## 🛠️ Setup & Reproducibility
Maintaining a stable environment for AI development is a primary focus. I have documented the entire bootstrap process, including hardware bridging and complex dependency resolutions (such as Intel MKL symbol conflicts).

👉 **[View the full Environment Setup Log (setup_log.md)](./docs/setup_log.md)**


## 📊 Data Pipeline (Updated 2026-02-10)
The Zombie Waves AI Codex is trained on a high-signal dataset engineered for conversational accuracy and hardware efficiency. The pipeline has evolved from static instructions to a multi-threaded, conversational architecture:

1. Acquisition & Extraction (Multi-Source)
   - **Reddit Intelligence:** Utilising the [Arctic Shift Download Tool](https://arctic-shift.photon-reddit.com/download-tool) for high-integrity exports of strategy-rich threads. This provides a baseline of peer-reviewed builds (e.g., MX Hero and Boreas meta).
   - **Discord Intelligence:** Targeted exports of the general-tips-n-tricks channels, capturing the "fast-meta" and real-time community troubleshooting.
   - **In-Game Codex:** (In Progress) Direct extraction of official weapon stats and ability definitions to act as the "Source of Truth."

2. Sanitisation & Safety
   - **Privacy Enforcement:** A custom Python layer programmatically strips PII (usernames/Discord IDs) and cross-references data against a local ID Blacklist to respect the "Right to Erasure."
   - **Content Filtering:** Integration of detox and antispam protocols during the Discord cleaning phase to ensure the Codex remains professional and focused, filtering out toxic language and bot-command noise.

3. Conversational Transformation (ChatML)
   - **The ChatML Pivot:** Unlike traditional static instruction pairs, all data is now transformed into ChatML format (System, User, Assistant).
   - **Contextual Pairing:** Discord message blocks are logically grouped to maintain conversational flow, while Reddit threads are karma-weighted to pair the most accurate expert response with the user's query.
   - **System Guardrails:** Every entry is anchored with a project-specific System Prompt to maintain persona integrity and domain focus.
  
4. Hardware-Aware Optimisation
   The pipeline incorporates specific memory-efficiency guardrails to facilitate training on consumer-grade GPUs (4GB VRAM). See [environment_setup.md](.docs/environment_setup.md) for full hardware configurations.

## 🚀 Current Status: Data Acquisition & Training

### ⚙️ System & Stack
- [x] **Hardware/GPU Integration:** RTX 3050 configured with proper CUDA drivers.
- [x] **Stable Linux Environment Setup:** WSL2/Ubuntu environment verified.
- [x] **Python AI Stack Configuration:** Unsloth, PyTorch, and dependencies installed.

### 📊 Data Pipeline
- [x] **Data Extraction:** Successfully extracted from 23-05-2023 - 03-02-2026 Snapshot.
- [x] **Data Cleaning:** Custom Regex & Nested List fixes applied to `clean-discord`.
- [ ] **YouTube Knowledge (Phase 2):** Transcript extraction and formatting.

### 🧪 Model Development
- 🔄 **Fine-Tuning Execution:** Currently in progress using Unsloth (LoRA adapters).
- [ ] **Model Evaluation:** Testing against known Zombie Waves strategy benchmarks.

## 📂 Project Structure

```text
ZombieWaves-AI-Codex/
├── docs/ # Documentation & Logs
├── tests/
├── legacy/ # Archived scripts
├── scripts/ # Helper scripts
├── data/ # Blacklist.txt
├── .gitignore # Prevents tracking of PII data and secrets
├── main.py <-- THE "BRAIN" 
└── README.md # Documentation & Ethics Statement
```

## ⚖️ Ethics & Compliance

This project is strictly for **personal research and educational purposes**. We prioritise data privacy and respect for the community through the following safeguards:

1. **Sourcing for Research:** Data is sourced from the Academic Torrents archive (Anonymised public dumps). This approach ensures zero impact on Reddit’s live infrastructure and follows established protocols for large-scale data science research.

2. **PII Sanitisation:** The project employs a "Signal over Identity" policy. All Personally Identifiable Information (PII)—including usernames, profile IDs, and specific timestamps—is stripped during the extraction phase. Our training datasets contain only game-mechanic text and strategic discussions.

3. **No Redistribution:** We do not redistribute the raw data dumps. The original archives are stored on a private, local drive and are used solely to generate the refined, anonymous knowledge base for the model.

4. **Right to Erasure Compliance:** While the dataset is a point-in-time snapshot, we prioritise the spirit of "User Deletion Rights." If specific content is identified as retracted or sensitive, it is programmatically purged from our training pipeline.

5. **Non-Commercial:** This project is entirely non-commercial. It is a technical showcase of AI fine-tuning and data engineering, not a product for sale or redistribution.

---

## 📜 Licence

Distributed under the MIT Licence. See LICENSE for more information.

## ⚠️ Disclaimer
**Project Codex** is an independent, non-commercial research project. It is not affiliated with, endorsed by, or officially connected to **Fun Formula**, **Reddit Inc.**, or any of their subsidiaries.

All product names, logos, and brands are property of their respective owners. The use of these names and brands does not imply endorsement. This tool is provided "as-is" for educational purposes, and the author assumes no liability for the accuracy of AI-generated strategies or game outcomes.
