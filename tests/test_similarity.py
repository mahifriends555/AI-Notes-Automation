

from app.embeddings.embedding_model import EmbeddingModel
from app.embeddings.similarity import SimilarityEngine


# Initialize model
embedding_model = EmbeddingModel()

# Initialize similarity engine
similarity_engine = SimilarityEngine()

# Sample texts
text1 = "Python basics"
text2 = "Python fundamentals"

# Generate embeddings
embedding1 = embedding_model.generate_embedding(text1)
embedding2 = embedding_model.generate_embedding(text2)

# Calculate similarity
score = similarity_engine.calculate_similarity(
    embedding1,
    embedding2
)

print(f"Similarity Score: {score}")


