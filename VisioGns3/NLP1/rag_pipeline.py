import chromadb
from sentence_transformers import SentenceTransformer


class RAGPipeline:
    """
    Simple local RAG pipeline:
    - Loads ChromaDB stored locally
    - Loads a local SentenceTransformer embedding model
    - Provides embed(), search(), and format_context()
    """

    def __init__(self, chroma_path: str, model_path: str):
        """
        Initialize RAG pipeline with:
        - chroma_path: folder where ChromaDB is stored
        - model_path: local folder of sentence-transformer model
        """

        print("[RAG] Loading embedding model...")
        self.model = SentenceTransformer(model_path)

        print("[RAG] Connecting to ChromaDB...")
        # FIX: Use PersistentClient instead of deprecated Client()
        self.client = chromadb.PersistentClient(path=chroma_path)

        # Load your existing collection
        self.collection = self.client.get_collection("network_docs")

        print("[RAG] RAG pipeline initialized successfully.\n")

    # ------------------------------------------------------------------

    def embed(self, text: str):
        """Return embedding vector for a piece of text."""
        return self.model.encode([text]).tolist()[0]

    # ------------------------------------------------------------------

    def search(self, query: str, top_k: int = 3):
        """
        Search ChromaDB:
        - Embed query
        - Retrieve nearest documents
        """
        q_emb = self.embed(query)

        results = self.collection.query(
            query_embeddings=[q_emb],
            n_results=top_k
        )

        return results

    # ------------------------------------------------------------------

    def format_context(self, results) -> str:
        """
        Convert retrieved docs into a single text block
        suitable for LLM prompting.
        """

        docs = results["documents"][0]
        scores = results["distances"][0]

        formatted = []
        for i, (doc, score) in enumerate(zip(docs, scores)):
            formatted.append(
                f"### Retrieved Document {i+1} (score={score})\n{doc}\n"
            )

        return "\n".join(formatted)
