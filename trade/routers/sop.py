from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
from ..repository import sop

router = APIRouter(
    prefix = '/sop',
    tags = ['SOP']
)

get_db = database.get_db

@router.post('/{id}', response_model = schemas.ShowSOPPlan)
def new_sop(id: int, request: schemas.NewSOP, db: Session = Depends(get_db), current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return sop.new_sop(id, request, db)

@router.get('/{id}', response_model = List[schemas.ShowSOPPlan])
def show_one_sop_plan(id: int, db: Session = Depends(get_db), current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return sop.show_one_sop_plan(id, db)

@router.get('/', response_model = List[schemas.ShowSOPPlan])
def show_all_sop_plan(db: Session = Depends(get_db), current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return sop.show_all_sop_plan(db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_sop_plan(id: int, db: Session = Depends(get_db), current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return sop.delete_sop_plan(id, db)



@router.post('/{id}', response_model = schemas.ShowSOP)
def latest_sop_update(id: int, request: schemas.LatestSOP, db: Session = Depends(get_db), current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return sop.latest_sop_update(id, request, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def revert_latest_sop_transaction(id: int, db: Session = Depends(get_db), current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return sop.revert_latest_sop_transaction(id, db)

@router.get('/{id}', response_model = schemas.ShowSOP)
def latest_sop(id: int, db: Session = Depends(get_db), current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return sop.latest_sop(id, db)