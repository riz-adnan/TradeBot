from sqlalchemy.orm import Session
from .. import mongodb, schemas
from fastapi import HTTPException, status
from ..hashing import Hash
from bson.objectid import ObjectId

users = mongodb.users
user_helper = mongodb.user_helper

async def create_user(request: schemas.GetUser):
    hashed_password = Hash.bcrypt(request.password)
    user = {
        "user_name": request.username,
        "email": request.email,
        "password": hashed_password,
        "api_key_private": request.api_key_private,
        "api_key_public": request.api_key_public,
        "base_url": request.base_url,
    }
    if users.find_one({"user_name": request.username}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with name {request.username} already registered")
    if users.find_one({"email": request.email}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email {request.email} already registered")
    if users.find_one({"api_key_private": request.api_key_private}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with the given private api key already registered")
    if users.find_one({"api_key_public": request.api_key_public}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with api key public {request.api_key_public} already registered")
    result = users.insert_one(user)
    new_user = users.find_one({"_id": result.inserted_id})
    return user_helper(new_user)

async def show_one_user(user_name: str):
    user = users.find_one({"user_name": user_name})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username {user_name} not found")
    return user_helper(user)

async def show_all_users():
    users_list = []
    users_data = users.find()
    for user in users_data:
        users_list.append(user_helper(user))
    if not users_list:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"No users found")
    return users_list

async def update_user(user_name: str, request: schemas.UpdateUser):
    user = users.find_one({"user_name": user_name})
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with username {user_name} not found.")
    new_details = dict(request)
    new_details['password'] = Hash.bcrypt(request.password)
    updated_details = users.update_one({"user_name": user_name}, {"$set": new_details})
    if not updated_details:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = f"Unable to update user with username {user_name}")
    updated_details = users.find_one({"user_name": user_name})
    return user_helper(updated_details)

async def show_user_detail(user_name: str):
    user = users.find_one({"user_name": user_name})
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"No users found")
    return user_helper(user)

async def delete_user(user_name: str):
    user = users.find_one({"user_name": user_name})
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id {id} not found")
    users.delete_one({"user_name": user_name})
    return 'Done'

async def show_all_users_detail():
    user_list = []
    users = users.find()
    for user in users:
        user_list.append(user_helper(user))
    if not user_list:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"No users found")
    return user_list