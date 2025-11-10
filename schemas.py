"""
Database Schemas for Galaxy Planner

Each Pydantic model corresponds to a MongoDB collection with the
collection name as the lowercase class name.
"""
from typing import Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime

# Calendar notes for a specific date (YYYY-MM-DD)
class Note(BaseModel):
    date: str = Field(..., description="ISO date, e.g., 2025-01-31")
    title: str = Field(..., description="Short note title")
    content: Optional[str] = Field(None, description="Detail of the note")

# Todo items per specific date
class Todo(BaseModel):
    date: str = Field(..., description="ISO date, e.g., 2025-01-31")
    text: str = Field(..., description="Task description")
    done: bool = Field(False, description="Completion status")

# Finance records (income/expense)
class Finance(BaseModel):
    date: str = Field(..., description="ISO date, e.g., 2025-01-31")
    type: Literal["income", "expense"] = Field(..., description="Record type")
    amount: float = Field(..., ge=0, description="Amount of the record")
    category: Optional[str] = Field(None, description="Category label")
    note: Optional[str] = Field(None, description="Optional memo")

# Photo library: store a title and an image data URL (base64) or remote URL
class Photo(BaseModel):
    title: Optional[str] = Field(None, description="Photo title")
    src: str = Field(..., description="Data URL (base64) or remote URL")
    date: Optional[str] = Field(None, description="Associated date")

# Dreams comes true list
class Dream(BaseModel):
    title: str = Field(..., description="Dream title")
    description: Optional[str] = Field(None, description="Why it matters")
    image: Optional[str] = Field(None, description="Image data URL or URL")
    achieved: bool = Field(False, description="Whether achieved")

# Reminders with datetime and optional link to a date
class Reminder(BaseModel):
    title: str = Field(..., description="Reminder title")
    datetime_iso: str = Field(..., description="ISO datetime string")
    message: Optional[str] = Field(None, description="Reminder message")
    date: Optional[str] = Field(None, description="Related calendar date (YYYY-MM-DD)")
