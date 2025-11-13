import os
import json
from pathlib import Path

# Optional dependency for token-based splitting
try:
    import tiktoken
    use_tiktoken = True
except ImportError:
    print("⚠️ tiktoken not installed — using character-based chunking instead.")
    use_tiktoken = False


# --- CONFIG --- #
BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
OUTPUT_FILE = BASE_DIR / "rag_preprocessed_chunks.json"

CHUNK_SIZE = 300      # token count if using tiktoken (~1000 chars fallback)
CHUNK_OVERLAP = 50    # overlap between chunks to preserve context


def read_all_docs(directory: Path):
    """Recursively read all .md and .json files in the knowledge_base directory."""
    docs = []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(".md") or f.endswith(".json"):
                file_path = Path(root) / f
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        text = file.read()
                        docs.append({"path": str(file_path), "text": text})
                except Exception as e:
                    print(f"⚠️ Error reading {file_path}: {e}")
    return docs


def chunk_text(text: str, chunk_size: int, overlap: int):
    """Split text into overlapping chunks (by tokens if possible, else by characters)."""
    if use_tiktoken:
        enc = tiktoken.get_encoding("cl100k_base")
        tokens = enc.encode(text)
        chunks = []
        for i in range(0, len(tokens), chunk_size - overlap):
            chunk = enc.decode(tokens[i:i + chunk_size])
            chunks.append(chunk)
        return chunks
    else:
        # Character-based fallback
        step = chunk_size * 4
        overlap_chars = overlap * 4
        chunks = []
        for i in range(0, len(text), step - overlap_chars):
            chunks.append(text[i:i + step])
        return chunks


def preprocess_docs():
    """Read all knowledge base files, chunk them, and store as JSON for embeddings."""
    print(f"🔍 Scanning knowledge base at: {KNOWLEDGE_BASE_DIR}")
    all_docs = read_all_docs(KNOWLEDGE_BASE_DIR)
    preprocessed = []

    for doc in all_docs:
        chunks = chunk_text(doc["text"], CHUNK_SIZE, CHUNK_OVERLAP)
        for i, chunk in enumerate(chunks):
            if chunk.strip():
                preprocessed.append({
                    "chunk_id": f"{Path(doc['path']).stem}_{i}",
                    "text": chunk.strip(),
                    "metadata": {
                        "source_file": Path(doc["path"]).name,
                        "source_path": doc["path"],
                        "chunk_index": i
                    }
                })

    # Save to output JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(preprocessed, f, indent=4, ensure_ascii=False)

    print(f"✅ {len(preprocessed)} chunks created and saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    preprocess_docs()
