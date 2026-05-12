
from app.core.database import SessionLocal

from app.db.crud import (
    create_note,
    get_note_by_id,
    get_all_notes
)


# Create database session
db = SessionLocal()


# -----------------------------
# CREATE NOTE
# -----------------------------
note = create_note(
    db=db,
    title="Python Basics",
    content="Python is a beginner-friendly programming language.",
    tags="python,programming"
)

print("\n✅ Note Created Successfully!")

print(f"ID: {note.id}")
print(f"Title: {note.title}")
print(f"Tags: {note.tags}")


# -----------------------------
# GET NOTE BY ID
# -----------------------------
fetched_note = get_note_by_id(
    db=db,
    note_id=note.id
)

print("\n📌 Fetched Single Note:")

if fetched_note:
    print(f"ID: {fetched_note.id}")
    print(f"Title: {fetched_note.title}")
    print(f"Content: {fetched_note.content}")
    print(f"Tags: {fetched_note.tags}")
else:
    print("Note not found.")


# -----------------------------
# GET ALL NOTES
# -----------------------------
all_notes = get_all_notes(db=db)

print("\n📚 All Notes:")

for note in all_notes:
    print(
        f"ID: {note.id} | "
        f"Title: {note.title} | "
        f"Tags: {note.tags}"
    )


# -----------------------------
# CLOSE DATABASE SESSION
# -----------------------------
db.close()

print("\n🔒 Database session closed.")
