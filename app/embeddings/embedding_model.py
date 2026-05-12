
from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    def __init__(self):
        """
        Load embedding model once during initialization.
        """

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        print("Embedding model loaded successfully!")

    def generate_embedding(self, text: str):
        """
        Convert text into vector embedding.
        """

        embedding = self.model.encode(text)

        return embedding

if __name__ == "__main__":
    # Example usage
    embedding_model = EmbeddingModel()
    text = "This is a sample text to generate an embedding."
    embedding = embedding_model.generate_embedding(text)
    print("Generated embedding:", embedding)