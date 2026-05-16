
# app/embeddings/chunking.py

class TextChunker:
    """
    Break text into meaningful chunks.
    """
    
    def __init__(self, chunk_size: int = 1000, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(self, text: str) -> list:
        """
        Split by paragraphs, not arbitrary size.
        """
        
        paragraphs = text.split('\n\n')
        chunks = []
        
        for para in paragraphs:
            if len(para) > self.chunk_size:
                # Split long paragraph into sentences
                sentences = para.split('. ')
                current_chunk = ""
                
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) < self.chunk_size:
                        current_chunk += sentence + ". "
                    else:
                        chunks.append(current_chunk.strip())
                        current_chunk = sentence + ". "
                
                if current_chunk:
                    chunks.append(current_chunk.strip())
            else:
                chunks.append(para.strip())
        
        return [c for c in chunks if c]  # Remove empty