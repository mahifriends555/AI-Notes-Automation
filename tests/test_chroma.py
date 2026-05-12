
from app.services.chroma_service import ChromaService


# Initialize service
chroma_service = ChromaService()

# Add notes
chroma_service.add_note(
    note_id="1",
    text="Python is a programming language"
)

chroma_service.add_note(
    note_id="2",
    text="Machine learning uses neural networks"
)

chroma_service.add_note(
    note_id="3",
    text="Football is a popular sport"
)

# Search
results = chroma_service.search_similar_notes(
    query="Python coding"
)

print(results)

