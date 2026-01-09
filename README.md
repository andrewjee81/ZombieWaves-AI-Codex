# 🧟 Project Codex: Zombie Waves AI Strategy Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CUDA Ready](https://img.shields.io/badge/CUDA-12.x-green.svg)](https://developer.nvidia.com/cuda-toolkit)

**Project Codex** is a non-commercial, educational research project designed to build a high-fidelity "Expert AI" for the mobile game *Zombie Waves*. By leveraging the official Reddit Data API and local fine-tuning on an NVIDIA-powered workstation, this project explores the intersection of community-driven game theory and Large Language Models (LLMs).

---

## 🚀 Overview

The goal of this project is to ingest unstructured community strategy data (synergies, hero builds, and game exploits) and transform it into a structured knowledge base for a specialized LLM. 

### Key Features
- **Automated Ingestion:** Uses PRAW to ethically collect high-signal strategy threads.
- **Data Refinement:** A "Teacher AI" pipeline that converts raw discussions into instruction-response JSONL pairs.
- **Local Fine-Tuning:** Optimized for NVIDIA RTX GPUs using the Unsloth/HuggingFace ecosystem.
- **SSD-Based Data Lake:** High-speed I/O management using an external 500GB SSD for training stability.

---

## 🛠️ Tech Stack & Rig
- **Platform:** Windows 11 (WSL2 / Ubuntu 22.04 LTS)
- **Hardware:** ASUS Gaming Laptop | NVIDIA RTX GPU | 500GB External SSD
- **Tools:** - [PRAW](https://praw.readthedocs.io/) (Reddit API Wrapper)
  - [Crawl4AI](https://crawl4ai.com/) (Web-to-Markdown Extraction)
  - [yt-dlp](https://github.com/yt-dlp/yt-dlp) (Video Transcript Analysis)

---

## ⚖️ Ethics & Compliance

This project is strictly for **personal research and educational purposes**. We prioritize platform integrity and user privacy:

1. **Official Channels:** Data collection is performed exclusively through the official Reddit Data API (PRAW).
2. **Rate Limiting:** Scripts are hard-coded to respect the 60 Requests Per Minute (RPM) limit.
3. **Privacy:** No Personally Identifiable Information (PII) is stored or used in the training process.
4. **Data Freshness:** Routine scripts are used to remove any content that has been deleted by users on the source platform.
5. **Non-Commercial:** The resulting models and datasets are not for sale or commercial distribution.

---

## 📂 Repository Structure

```text
ProjectCodex/
├── scrapers/           # PRAW and Web Extraction scripts
├── processing/         # Data cleaning & JSONL formatting
├── docs/               # Strategy logic & research notes
├── .gitignore          # Prevents pushing .env and local data
└── README.md           # Project Documentation
```

## 📜 License

Distributed under the MIT License. See LICENSE for more information.

Disclaimer: Project Codex is an independent project and is not affiliated with, endorsed by, or in any way officially connected with Fun Formula or Reddit Inc.
