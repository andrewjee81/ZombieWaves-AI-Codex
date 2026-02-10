## 📝 Technical Post-Mortem: AI Training Environment Setup
**Project:** ZombieWaves-AI-Codex  
**Hardware:** NVIDIA RTX 3050 (4GB VRAM)  
**Date:** February 2026  
**Status:** ✅ SUCCESSFUL VALIDATION RUN

## 1. The Core Conflict
The primary issue was a three-way version mismatch between the stable release of PyTorch (2.5.1), the new Unsloth 2026 update, and the hardware acceleration library `torchao`.

- **Error 1:** `AttributeError: module 'torch' has no attribute 'int1'`. This occurred because `torchao` attempted to use 1-bit quantization features introduced in PyTorch 2.6, but the environment was on 2.5.
- **Error 2:** `ResolutionImpossible`. Manual attempts to downgrade `transformers` to 4.47.1 failed because Unsloth 2026.1.4 has a hard dependency floor of `transformers >= 4.51.3`.

## 2. The "Nightly" Pivot
To fix the `int1` error, we moved from the stable PyTorch branch to the **Nightly (Preview)** build. This provided the necessary C++ headers for the new data types.

- **Command:** ```bash
  pip install --pre torch torchvision torchaudio --index-url [https://download.pytorch.org/whl/nightly/cu121](https://download.pytorch.org/whl/nightly/cu121) --force-reinstall```

3. The Triton Optimization Bug
After the Nightly install, a new error appeared: `RuntimeError: Unexpected optimization option triton.enable_persistent_tma_matmul`.

Cause: The Unsloth `GRPOTrainer` (Reinforcement Learning) was attempting to use an experimental Triton flag not yet supported by the specific Nightly build installed.

Impact: This crashed the entire `unsloth` import process, even for standard training.

4. Surgical Bypass (The "Dummy" File)
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

## 🎓 Learning Resources & Credits

This project follows the modern 'Local LLM Fine-Tuning' pipeline. I am by no means an expert; like many of you, I am learning as I go. If you are new to AI training, I highly recommend the following resources that were instrumental in helping me understand and implement this project:  

### 📺 Key Video Tutorials
* **[How to Fine-Tune Llama 3 Locally](https://www.youtube.com/watch?v=pxhkDaKzBaY)** - A comprehensive guide on the entire pipeline from data to local deployment.
* **[Unsloth: Formatting Datasets for Chat](https://www.youtube.com/watch?v=Lt7KrFMcCis)** - This was the catalyst for moving from Alpaca to ChatML. It explains how 'Supervised Fine-Tuning' (SFT) works better when the data follows a conversational role-based structure.
* **[Discord Data for AI](https://www.youtube.com/watch?v=Oms0D-A88JY)** - Understanding why data cleaning is the most critical step in the process.

### 📖 Essential Technical Reading
* **[The Case for ChatML (OpenAI Standard)](https://github.com/openai/openai-python/blob/main/chatml.md):** I transitioned from the Alpaca instruction format to **ChatML** after researching how modern LLMs handle roles (`system`, `user`, `assistant`). This documentation explains the security and clarity benefits of separating instructions from content.
* **[Unsloth Chat Templates Documentation](https://unsloth.ai/docs/basics/chat-templates):** This resource was instrumental in aligning our `master_codex_data.jsonl` with the native Llama-3-Instruct format to ensure the model maintains its 'Expert Strategy Assistant' persona.

### 🛠️ Core Technologies Used
* **[Unsloth AI](https://github.com/unslothai/unsloth):** Used for 2x faster, 80% less memory fine-tuning on consumer GPUs.
* **[DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter):** The gold standard for extracting raw community knowledge.
* **[Clean-Discord (Forked)](https://github.com/andrewjee81/clean-discord):** Modified to support modern 19-digit Discord IDs and nested structures.
* **[Scraping YouTube with OpenAI (Eli the Computer Guy)](https://www.youtube.com/watch?v=2TL3DgIMY1g):** Provided the logic for our YouTube Transcript Chunker, converting long-form video audio into structured strategy pairs.
