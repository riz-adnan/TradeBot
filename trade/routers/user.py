from typing import List
from fastapi import APIRouter, Depends, status
from .. import database, schemas, models, oauth2
from sqlalchemy.orm import Session
from ..repository import user

router = APIRouter(
    prefix = '/user',
    tags = ['user']
)
get_db = database.get_db


@router.post('/', response_model = schemas.ShowUser, status_code = status.HTTP_201_CREATED)
def create_user(request: schemas.GetUser, db: Session = Depends(get_db)):
    return user.create_user(request, db)

@router.get('/{id}', response_model = schemas.ShowUser, status_code = status.HTTP_200_OK)
def show_user(id: int, db: Session = Depends(get_db)):
    return user.show_one_user(id, db)

@router.get('/', response_model = List[schemas.ShowUser], status_code = status.HTTP_200_OK)
def all_users(db: Session = Depends(get_db)):
    return user.show_all_users(db)

@router.put('/{id}', response_model = schemas.ShowUser, status_code = status.HTTP_202_ACCEPTED)
def update_user(id: int, request: schemas.UpdateUser, db: Session = Depends(get_db), current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return user.update_user(id, request, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return user.delete_user(id, db)

@router.get('/{id}/details', response_model = schemas.UserDetails, status_code = status.HTTP_200_OK)
def user_detail(id: int, db: Session = Depends(get_db), current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return user.show_user_detail(id, db)

@router.get('/', response_model = List[schemas.UserDetails], status_code = status.HTTP_200_OK)
def all_users_detail(db: Session = Depends(get_db), current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return user.show_all_users_detail(db)