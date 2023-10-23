from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
from ..repository import investment

router = APIRouter(
    prefix = '/investment',
    tags = ['Investment']
)

get_db = database.get_db

@router.post('/', response_model = schemas.ShowInvestment)
def new_investment(id: int, request: schemas.UpdateInvestment, db: Session = Depends(get_db), current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return investment.new_investment(id, request, db)

@router.get('/{id}', response_model = List[schemas.ShowInvestment])
def show_ones_investment(id: int, db: Session = Depends(get_db), current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return investment.show_ones_investment(id, db)

@router.get('/', response_model = List[schemas.ShowInvestment])
def show_all_investment(db: Session = Depends(get_db), current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return investment.show_all_investment(db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def revert_latest_investment(id: int, db: Session = Depends(get_db), current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return investment.revert_latest_investment(id, db)