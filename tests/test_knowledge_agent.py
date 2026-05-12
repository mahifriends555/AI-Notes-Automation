

from app.agents.knowledge_agent import KnowledgeAgent


agent = KnowledgeAgent()

# First note
result1 = agent.process_note(
    note_id="1",
    text="Python basics and programming fundamentals"
)

print(result1)

# Similar note
result2 = agent.process_note(
    note_id="2",
    text="Introduction to Python programming"
)

print(result2)

# Different note
result3 = agent.process_note(
    note_id="3",
    text="Football world cup match analysis"
)

print(result3)
