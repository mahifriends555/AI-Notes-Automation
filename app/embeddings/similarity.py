
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class SimilarityEngine:
    def calculate_similarity(
        self,
        embedding1,
        embedding2
    ) -> float:
        """
        Calculate cosine similarity between two embeddings.
        """

        # Reshape vectors into 2D arrays
        embedding1 = np.array(embedding1).reshape(1, -1)
        embedding2 = np.array(embedding2).reshape(1, -1)

        similarity_score = cosine_similarity(
            embedding1,
            embedding2
        )[0][0]

        return float(similarity_score)
    
if __name__ == "__main__":
    # Example usage
    embedding1 = [0.1, 0.2, 0.3]
    embedding2 = [-0.7, 0.2, 0.3]
    similarity_engine = SimilarityEngine()
    similarity_score = similarity_engine.calculate_similarity(
        embedding1,
        embedding2
    )
    print("Cosine Similarity Score:", similarity_score)
