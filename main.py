import os
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Note, Todo, Finance, Photo, Dream, Reminder

app = FastAPI(title="Galaxy Planner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Galaxy Planner API running"}

@app.get("/test")
def test_database():
    status = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "collections": []
    }
    try:
        if db is not None:
            status["database"] = "✅ Connected"
            status["collections"] = db.list_collection_names()
    except Exception as e:
        status["database"] = f"❌ Error: {str(e)}"
    return status

# ---------- Helpers ----------
class IDModel(BaseModel):
    id: str

# ---------- Notes ----------
@app.post("/notes")
def add_note(note: Note):
    note_id = create_document("note", note)
    return {"id": note_id}

@app.get("/notes")
def list_notes(date: Optional[str] = None):
    filt = {"date": date} if date else {}
    items = get_documents("note", filt)
    for it in items:
        it["id"] = str(it.pop("_id"))
    return items

# ---------- Todos ----------
@app.post("/todos")
def add_todo(todo: Todo):
    todo_id = create_document("todo", todo)
    return {"id": todo_id}

@app.get("/todos")
def list_todos(date: Optional[str] = None):
    filt = {"date": date} if date else {}
    items = get_documents("todo", filt)
    for it in items:
        it["id"] = str(it.pop("_id"))
    return items

# ---------- Finance ----------
@app.post("/finance")
def add_finance(rec: Finance):
    rec_id = create_document("finance", rec)
    return {"id": rec_id}

@app.get("/finance")
def list_finance(date: Optional[str] = None, type: Optional[str] = None):
    filt = {}
    if date:
        filt["date"] = date
    if type in ("income", "expense"):
        filt["type"] = type
    items = get_documents("finance", filt)
    for it in items:
        it["id"] = str(it.pop("_id"))
    return items

# ---------- Photos ----------
@app.post("/photos")
def add_photo(photo: Photo):
    photo_id = create_document("photo", photo)
    return {"id": photo_id}

@app.get("/photos")
def list_photos(date: Optional[str] = None):
    filt = {"date": date} if date else {}
    items = get_documents("photo", filt)
    for it in items:
        it["id"] = str(it.pop("_id"))
    return items

# ---------- Dreams ----------
@app.post("/dreams")
def add_dream(dream: Dream):
    dream_id = create_document("dream", dream)
    return {"id": dream_id}

@app.get("/dreams")
def list_dreams():
    items = get_documents("dream")
    for it in items:
        it["id"] = str(it.pop("_id"))
    return items

# ---------- Reminders ----------
@app.post("/reminders")
def add_reminder(rem: Reminder):
    rem_id = create_document("reminder", rem)
    return {"id": rem_id}

@app.get("/reminders")
def list_reminders(date: Optional[str] = None):
    filt = {"date": date} if date else {}
    items = get_documents("reminder", filt)
    for it in items:
        it["id"] = str(it.pop("_id"))
    return items

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
