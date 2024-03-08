from pydantic import BaseModel
from datetime import datetime


class CreateToken(BaseModel):
    username: str
    token: str


class NoteInfoResponse(BaseModel):
    created_at: datetime
    updated_at: datetime


class NoteTextResponse(BaseModel):
    id: str
    text: str


class CreateNoteResponse(BaseModel):
    id: str


class ListNotesResponse(BaseModel):
    notes: dict


class CreateNoteRequest(BaseModel):
    text: str


class UpdateNoteRequest(BaseModel):
    text: str
