## ✅ Training Validation (First Contact)
Date: 2026-02-04

Target Model: Llama-3.2-3B-Instruct (4-bit)

Step Count: 60 (Test Run)

Outcome: SUCCESS

Final Loss: 3.6442

VRAM Peak: ~3.8GB (Stable)

Key Discovery: The 3050 (4GB) can handle a max_seq_length of 2048 at batch_size=1 with Unsloth optimizations.

Note: Did a simple prompt and the results was more chatter type, typical of Reddit conversations. To overcome this I have a "de-Reddit" script by stripping out those first-person phrases. Hopefully this makes the model sound much more authoritative.


## 🚀 TRAINING COMPLETE: 1,000 STEP MILESTONE REACHED 

Date: 2026-02-05

Project: ZombieWaves-AI-Codex

Hardware: NVIDIA RTX 3050 (4GB VRAM)

Total Time: ~1.92 Hours (6905.5s)

Efficiency: 2.31 samples/sec

Final Loss: 3.0602