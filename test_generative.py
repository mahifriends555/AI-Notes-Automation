"""
Test generative LLM behavior
LLM generates notes from topics
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from app.agents.formatting_agent import FormattingAgent
from app.services.chroma_service import ChromaService
from app.db.crud import create_note
from app.core.database import SessionLocal
import json

class GenerativeNoteSystem:
    """
    LLM autonomously generates notes from topics
    """
    
    def __init__(self):
        print("🚀 Initializing Generative Note System...\n")
        self.formatter = FormattingAgent()
        self.chroma = ChromaService()
        self.db = SessionLocal()
    
    def generate_note_from_topic(self, topic: str):
        """
        Given a topic, LLM generates a complete note
        """
        
        print(f"\n{'='*70}")
        print(f"🤖 GENERATING NOTE FROM TOPIC")
        print(f"Topic: {topic}")
        print(f"{'='*70}\n")
        
        try:
            # Step 1: Check for similar notes
            print("🔍 Searching for similar notes...")
            similar = self.chroma.search_similar_notes(topic, top_k=1)
            similar_notes = []
            if similar and similar.get('documents'):
                similar_notes = similar.get('documents', [[]])[0]
            
            if similar_notes:
                print(f"✅ Found similar note")
            else:
                print("✅ No similar notes found - generating new")
            
            # Step 2: LLM generates complete note
            print("🤖 LLM generating note...")
            generated = self.formatter.generate_note(topic, similar_notes)
            print("✅ Note generated")
            
            # Step 3: Save to database
            print("💾 Saving to database...")
            saved = create_note(
                self.db,
                title=generated.get('title', 'Untitled'),
                content=generated.get('content', ''),
                tags=json.dumps(generated.get('tags', [])),
                source="llm_generated",
                topic=topic,
                importance=0.8
            )
            print(f"✅ Saved (ID: {saved.id})")
            
            # Step 4: Add to vector DB
            self.chroma.add_note(str(saved.id), generated.get('content', ''))
            print("✅ Added to vector database")
            
            print(f"\n{'='*70}")
            print(f"✅ NOTE GENERATED SUCCESSFULLY")
            print(f"{'='*70}\n")
            
            return {
                "success": True,
                "note_id": saved.id,
                "generated_note": generated,
                "message": "Note generated and saved"
            }
        
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate note"
            }


# TEST EXECUTION
if __name__ == "__main__":
    
    system = GenerativeNoteSystem()
    
    # Test topics
    topics = [
        "Machine Learning Basics",
        "Python Decorators",
        "RESTful APIs Design"
    ]
    
    for topic in topics:
        result = system.generate_note_from_topic(topic)
        
        if result['success']:
            note = result['generated_note']
            print(f"\n📝 GENERATED NOTE:")
            print(f"Title: {note['title']}")
            print(f"Content: {note['content'][:300]}...")
            print(f"Keywords: {note.get('keywords', [])}")
            print(f"Tags: {note.get('tags', [])}")
            print(f"Summary: {note.get('summary', '')}")
        else:
            print(f"\n❌ Failed: {result['error']}")
        
        print("\n" + "="*70 + "\n")
