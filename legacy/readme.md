# 🏺 Legacy Data Utilities (Archived)

## Overview
This directory contains the original scripts used during the **Alpaca Era** of the Zombie Waves AI Codex. These tools were foundational in migrating the project from raw community data to a structured AI training format.

## Archived Components
- `alpaca_to_chatml.py`: Converted the initial Instruction/Response pairs into the current System/User/Assistant format.
- `noise_filter_v1.py`: Early regex-based cleaning (superseded by the Qwen 2.5 3B Judge).
- `jsonl_merger.py`: Used to combine Discord and Reddit exports before the integrated v6.1 pipeline was established.

## ⚠️ Warning
These scripts do not support **TurboQuant+** or **QJL error correction** and are preserved for documentation and research provenance only. For current production workflows, refer to the root `main.py`.