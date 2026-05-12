
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
