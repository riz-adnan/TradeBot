from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status
from ..hashing import Hash

def create_user(request: schemas.GetUser, db: Session):
    new_user = models.Users(user_name = request.username, email = request.email, password = Hash.bcrypt(request.password), api_key_public = request.api_key_public, api_key_private = request.api_key_private, base_url = request.base_url)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show_one_user(id: int, db: Session):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id {id} not found")
    return user

def show_all_users(db: Session):
    users = db.query(models.Users).all()
    if not users:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"No users found")
    return users

def update_user(id: int, request: schemas.UpdateUser, db: Session):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id {id} not found")
    user.update(email = request.email, password = Hash.bcrypt(request.password), api_key_public = request.api_key_public, api_key_private = request.api_key_private, base_url = request.base_url)
    db.commit()
    return 'updated'

def show_user_detail(id: int, db: Session):
    users = db.query(models.Users).filter(models.Users.id == id).first()
    if not users:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"No users found")
    return users

def delete_user(id: int, db: Session):
    user = db.query(models.Users).filter(models.Users.id == id)
    if not user.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id {id} not found")
    user.delete(synchronize_session = False)
    db.commit()
    return 'done'

def show_all_users_detail(db: Session):
    users = db.query(models.Users).all()
    if not users:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"No users found")
    return users