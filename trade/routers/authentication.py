from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..import schemas, token, mongodb
from .. hashing import Hash
from sqlalchemy.orm import Session

router = APIRouter(
    tags = ['Authentication']
)

users = mongodb.users
user_helper = mongodb.user_helper

@router.post('/login', status_code = status.HTTP_200_OK)
async def login(request: OAuth2PasswordRequestForm = Depends()):
    user = users.find_one({"email": request.username})
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Invalid Credentials')
    if not Hash.verify(user['password'], request.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Incorrect Password')
    # Generate a JWT token and return it
    access_token = token.create_access_token(data={"sub": user['email']})
    return {"access_token": access_token, "token_type": "bearer"}