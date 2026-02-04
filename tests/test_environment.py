import os

def check_environment():
    paths = {
        "Project Root (C:)": "/mnt/c/inetpub/wwwroot/GitHub/ZombieWaves-AI-Codex",
        "External Data (D:)": "/mnt/d/Project Codex",
        "Raw Comments": "/mnt/d/Project Codex/r_zombiewaves_comments.jsonl"
    }
    
    print("🔍 Running Environment Diagnostics...\n")
    for name, path in paths.items():
        if os.path.exists(path):
            print(f"✅ {name}: FOUND")
        else:
            print(f"❌ {name}: NOT FOUND (Check mount or path)")

if __name__ == "__main__":
    check_environment()