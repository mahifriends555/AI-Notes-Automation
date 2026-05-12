
import chromadb
from app.embeddings.embedding_model import EmbeddingModel


class ChromaService:

    def __init__(self):

        # Initialize embedding model
        self.embedding_model = EmbeddingModel()

        # Create persistent ChromaDB client
        self.client = chromadb.PersistentClient(
            path="data/chroma_db"
        )

        # Create or load collection
        self.collection = self.client.get_or_create_collection(
            name="notes"
        )

        print("ChromaDB initialized successfully!")

    def add_note(
        self,
        note_id: str,
        text: str
    ):
        """
        Add note embedding to ChromaDB.
        """

        embedding = self.embedding_model.generate_embedding(text)

        self.collection.add(
            ids=[note_id],
            documents=[text],
            embeddings=[embedding.tolist()]
        )

        print(f"Note '{note_id}' added successfully!")

    def search_similar_notes(
        self,
        query: str,
        top_k: int = 3
    ):
        """
        Search similar notes using semantic similarity.
        """

        query_embedding = self.embedding_model.generate_embedding(query)

        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )

        return results

