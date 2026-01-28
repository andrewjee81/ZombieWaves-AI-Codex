# Project Codex: Environment Bootstrap Log
**Author:** andrewjee81  
**Target System:** ASUS Gaming Rig (RTX GPU)  
**Environment:** WSL2 / Ubuntu 24.04 LTS

## 1. System Initialization (Windows Side)
The first step is to enable the Windows Subsystem for Linux (WSL2) and ensure the hardware drivers are bridged.

```powershell
# Run in PowerShell as Administrator
wsl --install -d Ubuntu-24.04
wsl --set-default Ubuntu-24.04
```

## 2. Storage Architecture
To handle the massive Reddit datasets, a portable SSD is bridged to the Linux filesystem.

```Bash
# In Ubuntu Terminal
sudo mkdir -p /mnt/d
sudo mount -t drvfs D: /mnt/d
```

## 3. Hardware Acceleration (NVIDIA CUDA)
The project leverages an NVIDIA RTX GPU via WSL2 passthrough.

```Bash

nvidia-smi
```

Confirmed: GPU visible and communicating with Ubuntu.

## 4. Python Environment Setup
We utilize Miniconda to create an isolated environment for the AI model.

```Bash

# Installation
wget [https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh](https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh)
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc

# Accept Conda Terms of Service (Required in 2026)
conda tos accept --override-channels --channel [https://repo.anaconda.com/pkgs/main](https://repo.anaconda.com/pkgs/main)
conda tos accept --override-channels --channel [https://repo.anaconda.com/pkgs/r](https://repo.anaconda.com/pkgs/r)
```

## 🛠️ 5. Troubleshooting & Bug Fixes
This section documents non-trivial issues encountered during the setup and the applied solutions.

**Issue A: Conda Terms of Service (TOS) Requirement**
**Error:** CondaToSNonInteractiveError: Terms of Service have not been accepted.

**Cause:** In late 2025, Anaconda introduced a mandatory manual acceptance of TOS for the main and r channels.

**Fix:** Explicitly accepted the channels via the CLI:

```Bash

conda tos accept --override-channels --channel [https://repo.anaconda.com/pkgs/main](https://repo.anaconda.com/pkgs/main)
```

**Issue B: Intel MKL Symbol Conflict (CRITICAL)**
**Error:** ImportError: ... libtorch_cpu.so: undefined symbol: iJIT_NotifyEvent

**Cause:** A version mismatch between the latest PyTorch binaries and the 2025/2026 Intel Math Kernel Library (MKL). PyTorch references a profiling symbol that was moved or removed in MKL versions >2024.1.

**Fix:** Downgraded the math libraries to the stable 2024 branch within the environment:

```Bash

conda install -y "mkl<2024.1" "intel-openmp<2024.1"
```

## 6. Final Validation
Final check to confirm PyTorch can access the GPU tensors:

```Bash

python -c "import torch; print('GPU Ready:', torch.cuda.is_available())"
```

Status: Success! (GPU Ready: True)