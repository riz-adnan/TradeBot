from typing import List
from fastapi import APIRouter, Depends, status
from .. import schemas, oauth2
from sqlalchemy.orm import Session
from ..repository import user

router = APIRouter(
    prefix = '/user',
    tags = ['user']
)


@router.post('/', response_model = schemas.ShowUser, status_code = status.HTTP_201_CREATED)
async def create_user(request: schemas.GetUser):
    return await user.create_user(request)

@router.get('/{user_name}', response_model = schemas.ShowUser, status_code = status.HTTP_200_OK)
async def show_user(user_name: str):
    return await user.show_one_user(user_name)

@router.get('/', response_model = List[schemas.ShowUser], status_code = status.HTTP_200_OK)
async def all_users(current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return await user.show_all_users()

@router.put('/{user_name}', response_model = schemas.ShowUser, status_code = status.HTTP_202_ACCEPTED)
async def update_user(user_name: str, request: schemas.UpdateUser, current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return await user.update_user(user_name, request)

@router.delete('/{user_name}', status_code = status.HTTP_204_NO_CONTENT)
async def delete_user(user_name: str, current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return await user.delete_user(user_name)

@router.get('/{user_name}/details', response_model = schemas.UserDetails, status_code = status.HTTP_200_OK)
async def user_detail(user_name: str, current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return await user.show_user_detail(user_name)

@router.get('/', response_model = List[schemas.UserDetails], status_code = status.HTTP_200_OK)
async def all_users_detail(current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return await user.show_all_users_detail()