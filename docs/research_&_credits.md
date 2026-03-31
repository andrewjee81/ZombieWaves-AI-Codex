# 📚 Learning Resources, Credits & Research

This document tracks the technical foundations and academic research that power the **Zombie Waves AI Codex**.

## 🧠 Core LLM Research
- **Google Research (March 24, 2026):** *TurboQuant+: Scaling Inference on Limited VRAM via PolarQuant & QJL.*
  - Key Application: Enabled the 6x KV Cache compression used to audit 226+ Codex entries on 4GB VRAM.
- **Alibaba Qwen Team:** Qwen 2.5 3B-Instruct methodology for high-fidelity technical extraction.

## 🛠️ Optimization Technologies
- **TurboQuant+ Engine:** Implemented via LMDeploy for hardware-aware inference.
- **Unsloth (FastLanguageModel):** Core framework for 4-bit LoRA fine-tuning.

## 🧟 Game Meta Sources
- **Zombie Waves Official Codex:** Direct weapon/hero stat extraction.
- **Arctic Shift:** Reddit/Discord data dumps for community-driven strategy.

This project follows the modern 'Local LLM Fine-Tuning' pipeline. I am by no means an expert; like many of you, I am learning as I go. If you are new to AI training, I highly recommend the following resources that were instrumental in helping me understand and implement this project:  

## 🔗 Model Resource
- [Qwen 3.5 Official Blog](https://qwen.ai/blog?id=qwen3.5): Documentation on the "Native Multimodal" architecture.

- [Hugging Face: Qwen3.5-35B-A3B](https://huggingface.co/Qwen/Qwen3.5-35B-A3B): The target repository for future fine-tuning.

- [Video: China’s Qwen 3.5 Shocked the AI World](https://www.youtube.com/watch?v=bd9Kca03Gpk): A technical breakdown of the MoE engine we will use for v8.1.

### 🧠 Core AI Theory & Mechanics
* **[How LLMs Actually Generate Text (LearnThatStack)](https://youtu.be/NKnZYvZA7w4?si=9X2JG-JljUm_8gBV):** A foundational guide explaining the mechanical "loop" of AI. It covers how text is converted into tokens and vectors, how the "Attention" mechanism focuses on context, and how the model uses probability to guess the next word one piece at a time. Essential for understanding why models hallucinate and how settings like "Temperature" influence the Codex's responses.
* **[The Case for ChatML (OpenAI Standard)](https://github.com/openai/openai-python/blob/main/chatml.md):** I transitioned from the Alpaca instruction format to **ChatML** after researching how modern LLMs handle roles (`system`, `user`, `assistant`). This documentation explains the security and clarity benefits of separating instructions from content.
* **[Unsloth: Formatting Datasets for Chat](https://www.youtube.com/watch?v=Lt7KrFMcCis):** This was the catalyst for moving from Alpaca to ChatML. It explains how 'Supervised Fine-Tuning' (SFT) works better when the data follows a conversational role-based structure.

### 🚀 The Qwen 3.5 "Agentic" Era
* **[Qwen 3.5: Towards Native Multimodal Agents (Official Blog)](https://qwen.ai/blog?id=qwen3.5):** Documentation on the "Native Multimodal" architecture. This provides the technical foundation for the MoE (Mixture of Experts) architecture and agentic capabilities.
* **[Video: China’s Qwen 3.5 Shocked the AI World](https://www.youtube.com/watch?v=bd9Kca03Gpk):** A technical breakdown of the MoE engine we will use for v8.1. Explains the A3B (Active 3 Billion) mechanism and how "Thinking Mode" enables complex ROI calculations for in-game resource spending.
* **[Hugging Face: Qwen3.5-35B-A3B](https://huggingface.co/Qwen/Qwen3.5-35B-A3B):** The target repository for future fine-tuning. This is the roadmap for fitting 35B-level reasoning into our 4GB VRAM limit.

### ⚙️ Hardware & Deployment
* **[Unsloth Chat Templates Documentation](https://unsloth.ai/docs/basics/chat-templates):** This resource was instrumental in aligning our `master_codex_data.jsonl` with the native Llama-3-Instruct format to ensure the model maintains its 'Expert Strategy Assistant' persona.
* **[How to Fine-Tune Llama 3 Locally](https://www.youtube.com/watch?v=pxhkDaKzBaY):** A comprehensive guide on the entire pipeline from data to local deployment.
* **[Discord Data for AI](https://www.youtube.com/watch?v=Oms0D-A88JY)** - Understanding why data cleaning is the most critical step in the process.

### 🛠️ Core Technologies Used
* **[Unsloth AI](https://github.com/unslothai/unsloth):** Used for 2x faster, 80% less memory fine-tuning on consumer GPUs.
* **[DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter):** The gold standard for extracting raw community knowledge.
* **[Clean-Discord (Forked)](https://github.com/andrewjee81/clean-discord):** Modified to support modern 19-digit Discord IDs and nested structures.
* **[Scraping YouTube with OpenAI (Eli the Computer Guy)](https://www.youtube.com/watch?v=2TL3DgIMY1g):** Provided the logic for our YouTube Transcript Chunker, converting long-form video audio into structured strategy pairs.
