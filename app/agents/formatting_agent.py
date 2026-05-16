from openai import OpenAI
import json
import os

class FormattingAgent:
    """
    LLM generates complete notes autonomously
    Not just formatting, but creating knowledge
    """
    
    def __init__(self, user_format: dict = None):
        api_key = os.getenv("OPENAI_API_KEY")
        
        self.client = OpenAI(api_key=api_key)
        self.format = user_format or {
            "title": "Clear title",
            "content": "Detailed content",
            "keywords": "Key terms",
            "examples": "Practical examples",
            "tags": "Categories"
        }
    
    def generate_note(self, topic: str, similar_notes: list = None) -> dict:
        """
        LLM GENERATES a complete note from a topic
        More autonomous and generative
        """
        
        context = ""
        if similar_notes:
            context = f"\n\nRelated existing knowledge:\n{similar_notes[0]}"
        
        prompt = f"""
You are an expert note-taking AI. Generate a comprehensive, well-structured note on this topic.

TOPIC: {topic}
{context}

Generate a COMPLETE note with this structure:
{{
    "title": "Clear, descriptive title",
    "content": "2-3 paragraphs of detailed content",
    "keywords": ["keyword1", "keyword2", "keyword3"],
    "examples": ["example1", "example2"],
    "tags": ["tag1", "tag2", "tag3"],
    "recall_words": "3-5 words for memory recall",
    "summary": "One sentence summary for quick recall"
}}

Make it:
- Educational and clear
- Include practical examples if you can
- Useful for learning and retention
- Well-organized and scannable

Return ONLY valid JSON.
"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        return json.loads(response.choices[0].message.content)