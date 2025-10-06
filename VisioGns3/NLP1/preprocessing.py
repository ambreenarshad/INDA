import json

# Input and output file names
input_file = "dataset_nlp1.json"
output_file = "dataset_nlp1_cleaned.json"

def preprocess_dataset(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned = []
    seen_prompts = set()

    for item in data:
        prompt = item.get("prompt", "").strip()
        machines = item.get("machines", [])
        connections = item.get("connections", [])

        # Skip if empty values
        if not prompt or not machines or not connections:
            continue

        # Skip duplicates by prompt
        if prompt in seen_prompts:
            continue
        seen_prompts.add(prompt)

        cleaned.append({
            "prompt": prompt,
            "machines": machines,
            "connections": connections
        })

    # Save cleaned dataset
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    print(f"Preprocessing complete ✅")
    print(f"Original size: {len(data)}, Cleaned size: {len(cleaned)}")
    print(f"Cleaned dataset saved as: {output_file}")

# Run preprocessing
preprocess_dataset(input_file, output_file)
