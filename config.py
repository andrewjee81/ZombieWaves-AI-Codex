import os
from dotenv import load_dotenv

load_dotenv()

# Filesystem
LOG_PATH = os.getenv("LOG_FILE_PATH")
EXT_ROOT_DIR = os.getenv("EXTERNAL_DRIVE_PATH")
EXT_MODEL_DIR = os.getenv("EXTERNAL_MODEL_PATH")
LOCAL_DATA_DIR = os.getenv("LOCAL_DATA_PATH")

# Codex
VERSION_NO = os.getenv("CODEX_VER_NO")
VERSION_NAME = "MASTER CODEX " / os.getenv("CODEX_VERSION").format(CODEX_VER_NO = VERSION_NO)
IDENTITY = os.getenv("CODEX_IDENTITY")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT").format(VERSION = VERSION_NAME, IDENTITY = IDENTITY)
TRAINING_DATA = f'training_master_v{VERSION_NO}_weighted.jsonl'
MODEL_FOLDER = f"final_codex_model_v{VERSION_NO}"
MODEL_PATH = os.path.join(EXT_MODEL_DIR, MODEL_FOLDER)

# Hardware/Train
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 1))
STEPS = int(os.getenv("STEPS", 1200))