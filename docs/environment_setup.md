## 📝 Technical Post-Mortem: AI Training Environment Setup
**Project:** ZombieWaves-AI-Codex  
**Hardware:** NVIDIA RTX 3050 (4GB VRAM)  
**Date:** February 2026  
**Status:** ✅ SUCCESSFUL VALIDATION RUN

## 1. The Core Conflict
The primary issue was a three-way version mismatch between the stable release of PyTorch (2.5.1), the new Unsloth 2026 update, and the hardware acceleration library `torchao`.

- **Error 1:** `AttributeError: module 'torch' has no attribute 'int1'`. This occurred because `torchao` attempted to use 1-bit quantization features introduced in PyTorch 2.6, but the environment was on 2.5.
- **Error 2:** `ResolutionImpossible`. Manual attempts to downgrade `transformers` to 4.47.1 failed because Unsloth 2026.1.4 has a hard dependency floor of `transformers >= 4.51.3`.

## 2. The "Nightly" Pivot (Updated 2026-03-28)
To fix the initial `int1` errors and enable **TurboQuant+ / QJL error correction**, we moved from the stable PyTorch branch to the **Nightly (Preview)** build.

- **Rationale:** Stable PyTorch releases (v2.5.x) lack the low-level bit-manipulation kernels required for the 6x KV Cache compression described in the [Research & Credits](./research_&_credits.md) document.
- **Hardware Synergy:** This pivot is mandatory for the RTX 3050 (4GB) to handle 8192-token sequences without "Truncation Errors."
- **Command:** ```bash
  pip install --pre torch torchvision torchaudio --index-url [https://download.pytorch.org/whl/nightly/cu121](https://download.pytorch.org/whl/nightly/cu121) --force-reinstall

## 3. The Triton Optimization Bug
After the Nightly install, a new error appeared: `RuntimeError: Unexpected optimization option triton.enable_persistent_tma_matmul`.

Cause: The Unsloth `GRPOTrainer` (Reinforcement Learning) was attempting to use an experimental Triton flag not yet supported by the specific Nightly build installed.

Impact: This crashed the entire `unsloth` import process, even for standard training.

## 4. Surgical Bypass (The "Dummy" File)
Since the project does not require Reinforcement Learning (RL) features, we manually disabled the broken module.

Move: Renamed the broken RL module: `mv .../unsloth/models/rl.py .../unsloth/models/rl.py.bak`

Stub: Recreated a "Dummy" `rl.py` to satisfy Python's import system.

Mocking: Injected a dummy function and class to prevent `ImportError`:

```Python

def PatchFastRL(**kwargs): pass
class vLLMSamplingParams: pass
```

**Note:** `vLLMSamplingParams` is mocked as a class rather than a variable to prevent `TypeError` during potential instantiation or isinstance checks within the Unsloth/TRL patching logic.


## 5. Final Stability Flags
To suppress version warnings and prevent the broken compiler from re-triggering, two environment variables were set:

- `UNSLOTH_SKIP_TORCHVISION_CHECK=1`

- `UNSLOTH_SKIP_COMPILER=1`

## 6. The TRL Entropy Bug
- **Error:** `TypeError: 'function' object is not subscriptable` during `trainer.train()`.
- **Cause:** `trl` version 0.13.0+ introduced a mandatory entropy calculation that is incompatible with Unsloth’s optimized "Fast Forward" logits.
- **Fix:** Force-downgraded `trl` to version 0.12.1.
- **Command:** `pip install trl==0.12.1 --no-deps`

## 🛠️ The "Recovery One-Liner"
If this environment ever breaks, the sequence to restore it is:

1. **System Prep:** `sudo apt update && sudo apt install build-essential -y`
2. **PyTorch:** Install PyTorch Nightly via the index URL.
3. **Unsloth:** Install `unsloth[base]` and `unsloth_zoo[base]` from GitHub.
4. **TRL Fix:** `pip install trl==0.12.1 --no-deps`  <-- IMPORTANT
5. **Patch:** Re-apply the `rl.py` dummy file patch.
6. **Flags:** Export the `SKIP` variables.

## 👤 User Management & Environment Standards
To maintain system stability and a "Clean Room" development cycle, all work is performed under a dedicated `codex` system profile. Within this profile, we maintain two distinct virtual environments to isolate dependencies:

* **`codex` Environment:** Used for general development, data cleaning, and running the YouTube/Discord scraping scripts.
* **`codex-train` Environment:** A high-performance, minimalist environment containing the `Unsloth`, `Torch`, and `Bitsandbytes` stack. This environment is strictly reserved for the "Burn" (Fine-Tuning) to ensure zero VRAM wastage from unnecessary libraries.

## ⚠️ The Golden Rules for RTX 3050 (4GB)
Context: Training a 3B model on 4GB VRAM is an "extreme" configuration. The following constraints must be maintained to prevent immediate `OOM` (Out of Memory) or `Triton` crashes.

1. The Patch Integrity Rule

   Standard `pip install` or `pip upgrade` commands will overwrite the "Dummy" RL module. * Action: If you ever update `unsloth`, you must immediately re-verify the `rl.py` dummy file.

   - Verification: Run `python -c "from unsloth.models.rl import PatchFastRL; print('Check Passed')"`

3. The Batch Size "Floor"

   Hardware limit is `per_device_train_batch_size = 1`. * Logic: Setting this to 2 or higher will immediately spike VRAM usage beyond 4GB.

   - Solution: To achieve higher stability, increase `gradient_accumulation_steps` (e.g., set to 16 to simulate a batch of 16).

3. The Compiler Bypass

   Always suppress the broken `torch.compile` and `torchvision` check. * Action: Ensure your shell or your `train.py` script always exports:

```Bash
    export UNSLOTH_SKIP_TORCHVISION_CHECK=1
    export UNSLOTH_SKIP_COMPILER=1
```

4. The 3.8GB Ceiling

   Monitor `nvidia-smi`. If VRAM spikes, reduce `max_seq_length` to 1024.

## 🛠️ Hardware-Aware Optimisation (4GB VRAM)
To support the "Golden Rules" above, the following structural optimisations are baked into the training pipeline to ensure the model stays within the physical limits of the 4GB card:

* **4-bit NormalFloat (NF4) Quantisation:** The model is loaded via `bitsandbytes` to reduce its memory footprint by ~70% while maintaining reasoning capabilities.
* **Gradient Checkpointing:** Enabled to trade compute speed for memory stability; it re-calculates activations rather than storing them in VRAM.
* **Sequence Capping:** Training inputs are strictly capped at a `max_seq_length` of 1024 tokens to keep the KV cache manageable.
* **LoRA Rank Tuning:** Rank ($r$) is set to 8 and Alpha to 16. This provides enough "mental depth" for strategy without bloating the trainable parameter count.

## 🛠️ Troubleshooting Log
Error: RuntimeError: Failed to find C compiler
Date: 2026-02-04

Cause: Triton (used by Unsloth) requires a C compiler to build GPU kernels on the fly. Fresh WSL/Ubuntu installs often lack gcc.

Fix: Installed the build-essential package.

```Bash

sudo apt update && sudo apt install build-essential -y
```

Status: Resolved. Training successfully initialized.

---
## 🗃️ Data Sources & Scope

Initially, this project was designed to leverage public Reddit data. However, to build a truly comprehensive **Zombie Waves AI Codex**, the scope has been expanded to include high-signal community knowledge from multiple platforms:

* **Reddit (Public Data):** General community discussions and high-level strategy threads.
* **Discord (Community Tips):** Granular, real-time advice from the "general-tips-n-tricks" channel.
* **YouTube (Video Transcripts):** Expert video guides converted to text via Python-based transcript extraction.

By combining these sources, the model gains a balanced perspective of both long-form theory (Reddit) and tactical, "on-the-ground" advice (Discord/YouTube).

## 📈 Model Evolution & Roadmap  
The AI Codex has transitioned through three major "engine" phases to balance high-fidelity strategy with the 4GB VRAM limit of the RTX 3050.

**Phase 1: The Foundation (v1 – v7.9)**
- **Model:** Llama-3.2-3B-Instruct-bnb-4bit

- **Role:** Initial validation of the "Judge" logic.

- **Key Achievement:** Proved that Unsloth and 4-bit quantization could run a 3B model on consumer hardware. Established the project's move from Alpaca to the ChatML architecture.

**Phase 2: The Logic Pivot (v7.9.1 – v8.0)**  
- **Model:** Qwen2.5-3B-Instruct

- **Role:** Current engine for the v8.0 "Discovery" pivot.

- **Why Qwen?** Improved handling of structured JSON and technical game nomenclature. It serves as the primary "Veteran Auditor" for mining the 10k Reddit trash logs.

**Phase 3: The Multimodal Oracle (v8.1+ Upgrade)**  
- **Model Shift:** Transition from standard LLMs to Qwen 2.5 Omni (4-bit) to enable visual-spatial reasoning (Hero/Gear screenshot analysis).

- **Hardware Optimization:** Utilizing TurboQuant+ and QJL error correction to maintain a 4096+ context window on an RTX 3050 (4GB).

- **The "Guide" Philosophy:** Moving away from agentic execution to focus on Deep-Context Strategy Auditing—transforming the model into the ultimate technical manual for the community.

- **Zero-Action Protocol:** Ensuring the system remains a "Read/Analyze/Advise" engine rather than an autonomous actor, preserving the project's educational research status.