from fastapi import APIRouter
from src.models import CreateToken
from jose import jwt

router = APIRouter()

# Секретный ключ для подписи JWT токена
SECRET_KEY = "ваш-секретный-ключ"
ALGORITHM = "HS256"


@router.post('/create_token', response_model=CreateToken)
def create_note(username: str):
    token = jwt.encode({"username": username}, SECRET_KEY, algorithm=ALGORITHM)
    print(token)

    try:
        with open("../src/tokens.json", "a+") as file:
            file.write(token + "\n")
    except Exception as e:
        return {"error": str(e)}

    return {"username": username, "token": token}