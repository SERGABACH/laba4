from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import APIKeyQuery
import os
from datetime import datetime
from src.models import NoteInfoResponse, NoteTextResponse, CreateNoteResponse, ListNotesResponse, CreateNoteRequest, \
    UpdateNoteRequest

router = APIRouter()


NOTES_FOLDER = "notes"
TOKENS_FILE = "../src/tokens.json"


if not os.path.exists(NOTES_FOLDER):
    os.makedirs(NOTES_FOLDER)

if not os.path.exists(TOKENS_FILE):
    with open(TOKENS_FILE, "w") as file:
        file.write("")

# Спецификация для API-ключа
api_key_query = APIKeyQuery(name='token', auto_error=False)


# Функция для проверки токена
def verify_token(token: str = Depends(api_key_query)):
    with open(TOKENS_FILE, "r") as file:
        tokens = file.read().splitlines()
        if token not in tokens:
            raise HTTPException(status_code=401, detail="Неверный токен")
    return token


# Метод для создания заметки
@router.post('/create_note', response_model=CreateNoteResponse)
def create_note(request: CreateNoteRequest, note_id: str, token: str = Depends(verify_token)):
    note_path = os.path.join(NOTES_FOLDER, f"{note_id}.txt")

    # Проверяем, существует ли заметка с указанным id
    if os.path.exists(note_path):
        raise HTTPException(status_code=400, detail="Заметка с таким id уже существует")

    with open(note_path, "w") as file:
        file.write(request.text.encode("UTF-8"))

    return {"id": note_id}


# Метод для вывода списка id заметок
@router.get('/list_notes', response_model=ListNotesResponse)
def list_notes(token: str = Depends(verify_token)):
    note_ids = [note.split('.')[0] for note in os.listdir(NOTES_FOLDER)]
    notes_dict = {i: int(note_id) for i, note_id in enumerate(note_ids)}
    return {"notes": notes_dict}


@router.get('/get_note_info/{note_id}', response_model=NoteInfoResponse)
def get_note_info(note_id: str, token: str = Depends(verify_token)):
    note_path = os.path.join(NOTES_FOLDER, f"{note_id}.txt")

    if not os.path.exists(note_path):
        raise HTTPException(status_code=404, detail="Заметка не найдена")

    created_time = os.path.getctime(note_path)
    modified_time = os.path.getmtime(note_path)

    return {"created_at": datetime.fromtimestamp(created_time).isoformat(), "updated_at": datetime.fromtimestamp(modified_time).isoformat()}


# Метод для чтения заметки по её id
@router.get('/read_note/{note_id}', response_model=NoteTextResponse)
def read_note(note_id: str, token: str = Depends(verify_token)):
    note_path = os.path.join(NOTES_FOLDER, f"{note_id}.txt")

    if not os.path.exists(note_path):
        raise HTTPException(status_code=404, detail="Заметка не найдена")

    with open(note_path, "r") as file:
        note_content = file.read()

    return {"id": note_id, "text": note_content}


# Метод для обновления текста заметки
@router.patch('/update_note/{note_id}', response_model=dict)
def update_note(note_id: str, request: UpdateNoteRequest, token: str = Depends(verify_token)):
    note_path = os.path.join(NOTES_FOLDER, f"{note_id}.txt")

    if not os.path.exists(note_path):
        raise HTTPException(status_code=404, detail="Заметка не найдена")

    with open(note_path, "w") as file:
        file.write(request.text)

    return {"message": "Заметка успешно обновлена"}


# Метод для удаления заметки
@router.delete('/delete_note/{note_id}')
def delete_note(note_id: str, token: str = Depends(verify_token)):
    note_path = os.path.join(NOTES_FOLDER, f"{note_id}.txt")

    if not os.path.exists(note_path):
        raise HTTPException(status_code=404, detail="Заметка не найдена")

    os.remove(note_path)

    return {"message": "Заметка успешно удалена"}
