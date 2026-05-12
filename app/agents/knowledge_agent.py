

from app.services.chroma_service import ChromaService


class KnowledgeAgent:

    def __init__(self):

        self.chroma_service = ChromaService()

        # Similarity threshold
        self.threshold = 0.80

    def process_note(
        self,
        note_id: str,
        text: str
    ):
        """
        Decide whether to CREATE or UPDATE note.
        """

        # Search similar notes
        results = self.chroma_service.search_similar_notes(
            query=text,
            top_k=1
        )

        documents = results.get("documents", [[]])[0]
        ids = results.get("ids", [[]])[0]
        distances = results.get("distances", [[]])[0]

        # No notes found
        if not documents:
            self.chroma_service.add_note(note_id, text)

            return {
                "action": "CREATE",
                "message": "New note created."
            }

        similarity_score = 1 - distances[0]

        print(f"Similarity Score: {similarity_score}")

        # Decide action
        if similarity_score >= self.threshold:

            return {
                "action": "UPDATE",
                "existing_note_id": ids[0],
                "similarity": similarity_score,
                "message": "Similar note found. Update existing note."
            }

        else:
            self.chroma_service.add_note(note_id, text)

            return {
                "action": "CREATE",
                "similarity": similarity_score,
                "message": "No similar note found. New note created."
            }

            