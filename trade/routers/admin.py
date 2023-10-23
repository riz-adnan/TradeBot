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

# @router.post('/', )