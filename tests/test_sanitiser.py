import sys
import os
# This line allows the test to "see" your scripts folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.sanitiser import sanitize_jsonl
import json

def test_noise_filter():
    input_file = "tests/mock_data.jsonl"
    output_file = "tests/test_output.jsonl"
    
    print("🧪 Testing Sanitizer Noise Filter...")
    
    # Run the sanitizer
    sanitize_jsonl(input_file, output_file)
    
    # Read the results
    with open(output_file, 'r') as f:
        results = [json.loads(line) for line in f]
    
    # ASSERTIONS (The "Pass/Fail" logic)
    # 1. We expect only 1 entry to remain
    assert len(results) == 1, f"❌ Expected 1 entry, but found {len(results)}"
    
    # 2. We expect the surviving entry to be 'test_1'
    assert results[0]['id'] == 'test_1', "❌ The wrong entry was kept!"
    
    # 3. We expect the author field to be GONE
    assert 'author' not in results[0], "❌ PII (author) was not stripped!"
    
    print("✅ Noise Filter Test Passed: PII stripped and 3 garbage entries removed.")

if __name__ == "__main__":
    test_noise_filter()