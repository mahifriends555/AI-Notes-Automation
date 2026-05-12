
from app.core.database import SessionLocal

from app.db.crud import create_note


# Create DB session
db = SessionLocal()

# Create note
note = create_note(
    db=db,
    title="Python Basics",
    content="Python is a beginner-friendly language.",
    tags="python,programming"
)

print("Note Created Successfully!")

print(f"ID: {note.id}")
print(f"Title: {note.title}")
print(f"Tags: {note.tags}")

# Close session
db.close()
