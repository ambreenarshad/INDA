#!/usr/bin/env python3
"""
prepare_training_data.py

This script converts a structured JSON dataset into JSONL format suitable for training a model.
Each line in the output file contains a "prompt" and the corresponding "response" (machines + connections).
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent

INPUT_FILE = BASE_DIR / "dataset_nlp1_cleaned.json"
OUTPUT_FILE = BASE_DIR / "training_data.jsonl"


def prepare_training_data(input_path: str, output_path: str):
    """
    Reads a JSON dataset and converts it to JSONL format for training.
    
    Args:
        input_path (str): Path to the input JSON file.
        output_path (str): Path to the output JSONL file.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Load JSON dataset
    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Open output JSONL file
    with output_path.open("w", encoding="utf-8") as out_f:
        for item in data:
            prompt = item.get("prompt", "").strip()
            machines = item.get("machines", [])
            connections = item.get("connections", [])

            response = json.dumps({"machines": machines, "connections": connections}, ensure_ascii=False)

            jsonl_item = {"prompt": prompt, "response": response}
            out_f.write(json.dumps(jsonl_item, ensure_ascii=False) + "\n")

    print(f"Training data prepared: {output_path} ({len(data)} samples)")

if __name__ == "__main__":
    prepare_training_data(INPUT_FILE, OUTPUT_FILE)
