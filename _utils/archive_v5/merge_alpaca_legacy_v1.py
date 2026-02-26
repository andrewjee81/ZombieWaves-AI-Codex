import os

# 1. Configuration
# Update this path if your files are in a different folder
DATA_FOLDER = '/mnt/c/inetpub/wwwroot/GitHub/ZombieWaves-AI-Codex/data'
OUTPUT_FILE = os.path.join(DATA_FOLDER, 'zombie_waves_master_codex.jsonl')

def merge_jsonl_files(input_folder, output_path):
    files_merged = 0
    total_lines = 0

    print(f"Starting merge in: {input_folder}")

    with open(output_path, 'w', encoding='utf-8') as outfile:
        # Loop through all files in the directory
        for filename in os.listdir(input_folder):
            # Only process .jsonl files and skip the output file itself
            if filename.endswith('.jsonl') and filename != os.path.basename(output_path):
                file_path = os.path.join(input_folder, filename)
                print(f"Merging: {filename}...")
                
                with open(file_path, 'r', encoding='utf-8') as infile:
                    for line in infile:
                        # Only write non-empty lines
                        if line.strip():
                            outfile.write(line.strip() + '\n')
                            total_lines += 1
                
                files_merged += 1

    print("---")
    print(f"Merge Complete!")
    print(f"Total Files Processed: {files_merged}")
    print(f"Total Training Examples: {total_lines}")
    print(f"Master File Created at: {output_path}")

if __name__ == "__main__":
    merge_jsonl_files(DATA_FOLDER, OUTPUT_FILE)