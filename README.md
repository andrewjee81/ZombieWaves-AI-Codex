# 🧟 Project Codex: Zombie Waves AI Strategy Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CUDA Ready](https://img.shields.io/badge/CUDA-12.x-green.svg)](https://developer.nvidia.com/cuda-toolkit)

**Project Codex** is a non-commercial, educational research project designed to build a high-fidelity "Expert AI" for the mobile game *Zombie Waves*. By leveraging the official Reddit Data API and local fine-tuning on an NVIDIA-powered workstation, this project explores community-driven game theory and Large Language Model (LLM) fine-tuning.

---

## 🚀 Overview

The goal of this project is to ingest unstructured community strategy data (synergies, hero builds, and game exploits) and transform it into a structured knowledge base for a specialized LLM.

### Key Features
- **Ethical Data Ingestion:** Uses PRAW to collect high-signal strategy threads via the official Reddit API.
- **Anonymized Processing:** Automated stripping of PII (Usernames/IDs) before local storage.
- **Compliance-First Design:** Hard-coded rate limiting (2s delays) and automated deletion sync logic.
- **Local Fine-Tuning:** Optimized for NVIDIA RTX GPUs using the Unsloth/HuggingFace ecosystem.

---

## 🛠️ Tech Stack & Rig
- **Hardware:** ASUS Gaming Rig | NVIDIA RTX GPU | 500GB External SSD
- **Platform:** Windows 11 (WSL2 / Ubuntu 22.04 LTS)
- **Primary Libraries:** PRAW, python-dotenv, PyTorch (CUDA 12.x)

---

## 📂 Project Structure

```text
ZombieWaves-AI-Codex/
├── data/               # Local symlink to E:/ External SSD (Data Lake)
├── .env                # API Keys & SSD Paths (Local only, Git-ignored)
├── .env.example        # Template for environment configuration
├── .gitignore          # Prevents tracking of PII data and secrets
├── requirements.txt    # Project dependencies (praw, python-dotenv)
├── scraper_skeleton.py # Main compliant extraction engine
└── README.md           # Documentation & Ethics Statement
```

---

## 📦 Installation & Deployment

Follow these steps to set up the environment on your local workstation.

### 1. Clone the Repository
```bash
git clone [https://github.com/andrewjee81/ZombieWaves-AI-Codex.git](https://github.com/andrewjee81/ZombieWaves-AI-Codex.git)
cd ZombieWaves-AI-Codex
```

### 2. Environment Configuration
Create a .env file in the root directory. Note: This file is ignored by git to protect API secrets.
```text
REDDIT_CLIENT_ID=your_id_here
REDDIT_CLIENT_SECRET=your_secret_here
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
SSD_DATA_PATH=E:/ZombieWavesProject/data/raw_reddit_data.jsonl
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Scraper
```bash
python scraper_skeleton.py
```

---

## ⚖️ Ethics & Compliance

This project is strictly for **personal research and educational purposes**. We prioritize platform integrity and user privacy through the following technical safeguards:

1. **Official Channels:** Data collection is performed exclusively through the official Reddit Data API using the PRAW library.
2. **Conservative Rate Limiting:** While the API allows 60 RPM, this script is hard-coded with a 2-second `REQUEST_DELAY` (30 RPM) to ensure zero impact on Reddit server stability.
3. **Anonymization by Design:** The `anonymize_data()` function strips all PII (usernames, IDs, timestamps) immediately upon ingestion. Only game-mechanic text is retained.
4. **Data Hygiene:** We retain `source_id` metadata solely to perform "Sync & Purge" checks. If content is deleted on Reddit, it is programmatically removed from our local research dataset to respect user deletion rights.
5. **Non-Commercial:** This project is not for sale, and no datasets will be redistributed or used for commercial gain.

---

## 📜 License

Distributed under the MIT License. See LICENSE for more information.

Disclaimer: Project Codex is an independent project and is not affiliated with, endorsed by, or in any way officially connected with Fun Formula or Reddit Inc.
