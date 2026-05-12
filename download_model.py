
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Download and save locally
model = SentenceTransformer(MODEL_NAME)

model.save("models/all-MiniLM-L6-v2")

print("Model downloaded and saved locally!")
