
from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../..')

from dotenv import load_dotenv
load_dotenv()

from app.agents.formatting_agent import FormattingAgent
from app.services.chroma_service import ChromaService
from app.db.crud import create_note, get_note_by_id, get_all_notes
from app.core.database import SessionLocal
import json

app = FastAPI(
    title="AI Notes API",
    description="Generate and manage AI notes",
    version="1.0"
)

# Request models
class GenerateNoteRequest(BaseModel):
    topic: str

class SearchRequest(BaseModel):
    query: str
    top_k: int = 3

# Initialize services
db = SessionLocal()
formatter = FormattingAgent()
chroma = ChromaService()


# ===================== ENDPOINTS =====================

@app.get("/")
def root():
    """Health check"""
    return {"status": "running", "message": "AI Notes API is alive"}


@app.post("/api/notes/generate")
def generate_note(request: GenerateNoteRequest):
    """Generate a new note from a topic"""
    
    similar = chroma.search_similar_notes(request.topic, top_k=1)
    similar_notes = []
    if similar and similar.get('documents'):
        similar_notes = similar.get('documents', [[]])[0]
    
    generated = formatter.generate_note(request.topic, similar_notes)
    
    saved = create_note(
        db,
        title=generated.get('title', 'Untitled'),
        content=generated.get('content', ''),
        tags=json.dumps(generated.get('tags', [])),
        source="api_generated",
        topic=request.topic,
        importance=0.8
    )
    
    chroma.add_note(str(saved.id), generated.get('content', ''))
    
    return {
        "success": True,
        "note_id": saved.id,
        "title": generated.get('title'),
        "summary": generated.get('summary', ''),
        "tags": generated.get('tags', [])
    }


@app.post("/api/notes/search")
def search_notes(request: SearchRequest):
    """Search for similar notes"""
    
    results = chroma.search_similar_notes(request.query, top_k=request.top_k)
    
    return {
        "success": True,
        "query": request.query,
        "results": results
    }


@app.get("/api/notes")
def list_all_notes():
    """Get all notes"""
    
    notes = get_all_notes(db)
    
    return {
        "success": True,
        "total": len(notes),
        "notes": [
            {
                "id": note.id,
                "title": note.title,
                "topic": note.topic,
                "created_at": str(note.created_at),
                "importance": note.importance
            }
            for note in notes
        ]
    }


@app.get("/api/notes/{note_id}")
def get_note(note_id: int):
    """Get a specific note by ID"""
    
    note = get_note_by_id(db, note_id)
    
    return {
        "success": True,
        "note": {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "tags": note.tags,
            "topic": note.topic,
            "created_at": str(note.created_at),
            "importance": note.importance
        }
    }


@app.get("/api/stats")
def get_stats():
    """Get system statistics"""
    
    all_notes = get_all_notes(db)
    
    stats = {
        "total_notes": len(all_notes),
        "by_topic": {},
        "by_source": {}
    }
    
    for note in all_notes:
        if note.topic not in stats["by_topic"]:
            stats["by_topic"][note.topic] = 0
        stats["by_topic"][note.topic] += 1
        
        if note.source not in stats["by_source"]:
            stats["by_source"][note.source] = 0
        stats["by_source"][note.source] += 1
    
    return {"success": True, "stats": stats}

