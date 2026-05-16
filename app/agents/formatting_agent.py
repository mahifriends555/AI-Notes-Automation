
from openai import OpenAI

class FormattingAgent:
    """
    NOT autonomous yet.
    Just converts text → formatted note.
    """
    
    def __init__(self, user_format: dict):
        self.client = OpenAI()
        self.format = user_format
    
    def format_note(self, text: str, similar_notes: list) -> dict:
        """
        Simple: Call OpenAI, return formatted.
        """
        
        context = ""
        if similar_notes:
            context = f"Similar note: {similar_notes[0]}"   # Just take the most similar one for context. Could be improved by taking more and summarizing them.
        
        prompt = f"""
        Format this note according to:
        {self.format}
        
        Content: {text}
        Context: {context}
        
        Return as JSON with keys:
        title, content, examples, tags, recall Words, Interview short summary
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)