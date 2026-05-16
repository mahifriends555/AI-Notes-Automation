# AI-Notes-Automation

**File: `README.md`**

```markdown
# AI Notes Automation

AI-powered note generation and management system.

## Features

- Generate complete notes from topics using OpenAI LLM
- Search similar notes using semantic similarity
- Store notes in SQLite database
- Vector storage with ChromaDB
- REST API endpoints

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Database

```bash
python create_db.py
```

### 3. Set Environment Variables

Create `.env` file:
```
OPENAI_API_KEY=your-api-key-here
```

## Run

### Generate Notes (Test)

```bash
python test_generative.py
```

### Start API Server

```bash
uvicorn app.api.main:app --reload
```

Then open:
```
http://localhost:8000/docs
```

## API Endpoints

### Generate Note
```
POST /api/notes/generate
Body: {"topic": "Python"}
```

### Search Notes
```
POST /api/notes/search
Body: {"query": "Python", "top_k": 3}
```

### Get All Notes
```
GET /api/notes
```

### Get One Note
```
GET /api/notes/{note_id}
```

### Get Stats
```
GET /api/stats
```

### Health Check
```
GET /
```

## Databases

### ChromaDB (Vector DB)
- Stores embeddings for semantic search
- Location: `data/chroma_db/`

### SQLite (Metadata DB)
- Stores note metadata (title, topic, created_at, etc)
- Location: `data/notes.db`

## Project Structure

```
AI-Notes-Automation/
├── app/
│   ├── agents/
│   │   ├── formatting_agent.py
│   │   └── knowledge_agent.py
│   ├── api/
│   │   └── main.py
│   ├── embeddings/
│   │   ├── chunking.py
│   │   ├── embedding_model.py
│   │   └── similarity.py
│   ├── services/
│   │   └── chroma_service.py
│   ├── db/
│   │   ├── models.py
│   │   └── crud.py
│   └── core/
│       └── database.py
├── data/
│   ├── chroma_db/
│   └── notes.db
├── main.py
├── test_generative.py
└── requirements.txt
```

## Requirements

- Python 3.10+
- OpenAI API key
- FastAPI
- ChromaDB
- SQLAlchemy
- Sentence Transformers

## Testing

### Test note generation:
```bash
python test_generative.py
```

### Test API:
```bash
# In browser: http://localhost:8000/docs

# Or with curl:
curl -X POST http://localhost:8000/api/notes/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "Python Basics"}'
```

## Next Steps

- Add PDF/YouTube input
- Add advanced retrieval (reranking)
- Build multi-agent system
- Add MCP integration

## Author

AI Notes Automation

## License

MIT
```

---

Copy this into `README.md` in your project root.