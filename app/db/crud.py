
from sqlalchemy.orm import Session

from app.db.models import Note


def create_note(
    db: Session,
    title: str,
    content: str,
    tags: str = None
):
    """
    Create and save a new note.
    """

    new_note = Note(
        title=title,
        content=content,
        tags=tags
    )

    db.add(new_note)

    db.commit()

    db.refresh(new_note)

    return new_note

def get_note_by_id(
    db: Session,
    note_id: int
):
    """
    Fetch single note by ID.
    """

    return db.query(Note).filter(
        Note.id == note_id
    ).first()

def get_all_notes(
    db: Session
):
    """
    Fetch all notes.
    """

    return db.query(Note).all()
