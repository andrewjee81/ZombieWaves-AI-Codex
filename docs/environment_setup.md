## 📝 Technical Post-Mortem: AI Training Environment Setup
**Project:** ZombieWaves-AI-Codex
**Hardware:** NVIDIA RTX 3050 (4GB VRAM)
**Date:** February 2026
**Status:** 🚀 ENGINE READY

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

## 🛠️ The "Recovery One-Liner"
If this environment ever breaks, the sequence to restore it is:

- **System Prep:** `sudo apt update && sudo apt install build-essential -y`

- **PyTorch:** Install PyTorch Nightly via the index URL above.

- **Unsloth:** Install `unsloth[base]` and `unsloth_zoo[base]` from GitHub.

- Patch: Re-apply the `rl.py` dummy file patch.

- Flags: Export the `SKIP` variables.

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

## 🛠️ Troubleshooting Log
Error: RuntimeError: Failed to find C compiler
Date: 2026-02-04

Cause: Triton (used by Unsloth) requires a C compiler to build GPU kernels on the fly. Fresh WSL/Ubuntu installs often lack gcc.

Fix: Installed the build-essential package.

```Bash

sudo apt update && sudo apt install build-essential -y
```

Status: Resolved. Training successfully initialized.
