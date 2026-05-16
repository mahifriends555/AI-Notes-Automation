
# main.py - ORCHESTRATION/INTEGRATION

"""
Main Entry Point - Complete Pipeline Integration
AI-Notes Automation System
"""

# LOAD ENV VARIABLES FIRST
import os
from dotenv import load_dotenv
load_dotenv()  # Load BEFORE anything else

import sys
import uuid
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# NOW import agents (which use OpenAI)
from app.agents.knowledge_agent import KnowledgeAgent
from app.agents.formatting_agent import FormattingAgent
from app.embeddings.chunking import TextChunker
from app.services.chroma_service import ChromaService
from app.db.crud import create_note
from app.core.database import SessionLocal


class NoteProcessingPipeline:
    """
    Complete end-to-end pipeline
    """
    
    def __init__(self, user_format: dict):
        self.knowledge_agent = KnowledgeAgent()
        self.formatter = FormattingAgent(user_format)
        self.chunker = TextChunker()
        self.chroma = ChromaService()
        self.db = SessionLocal()
    
    def process_user_input(self, user_input: str) -> dict:
        """
        Complete flow: Input → Output
        """
        
        print(f"\n{'='*60}")
        print(f"🚀 PROCESSING USER INPUT")
        print(f"{'='*60}\n")
        
        try:
            # Step 1: Chunk the input
            chunks = self.chunker.chunk_text(user_input)
            print(f"✅ Chunked into {len(chunks)} parts")
            
            # Step 2: Get decision (CREATE or UPDATE)
            note_id = str(uuid.uuid4())[:8]
            decision = self.knowledge_agent.process_note(note_id, user_input)
            print(f"✅ Decision: {decision['action']}")
            
            # Get similar notes for context
            similar = self.chroma.search_similar_notes(user_input, top_k=1)
            similar_notes = similar.get('documents', [[]])[0] if similar.get('documents', [[]])[0] else []
            
            # Step 3: Format the note
            formatted = self.formatter.format_note(user_input, similar_notes)
            print(f"✅ Note formatted")
            
            # Step 4: Save to database
            saved = create_note(
                self.db,
                title=formatted.get('title', 'Untitled'),
                content=formatted.get('content', user_input),
                tags=str(formatted.get('tags', [])),
                source="user_input",
                topic=formatted.get('topic', 'general'),
                importance=0.7
            )
            print(f"✅ Saved to database (ID: {saved.id})")
            
            # Step 5: Add to vector DB
            self.chroma.add_note(str(saved.id), formatted.get('content', user_input))
            print(f"✅ Added to vector database")
            
            print(f"\n{'='*60}")
            print(f"✅ PIPELINE COMPLETE")
            print(f"{'='*60}\n")
            
            return {
                "success": True,
                "action": decision['action'],
                "note_id": saved.id,
                "title": formatted.get('title'),
                "message": "Note processed successfully"
            }
        
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to process note"
            }


# MAIN EXECUTION
if __name__ == "__main__":
    
    user_format = {
        "title": "Clear, descriptive title",
        "content": "Main content",
        "keywords": "3-5 key terms",
        "tags": "Categories",
        "examples": "Practical examples"
    }
    
    pipeline = NoteProcessingPipeline(user_format)
    
    # Test input
    test_input = "Python functions are reusable blocks of code that perform specific tasks"
    
    result = pipeline.process_user_input(test_input)
    
    print("📝 RESULT:")
    print(result)
