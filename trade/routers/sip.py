from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
from ..repository import sip

router = APIRouter(
    prefix = '/sip',
    tags = ['SIP']
)

get_db = database.get_db

@router.post('/{id}', response_model = schemas.ShowSIPPlan)
def new_sip(id: int, request: schemas.NewSIP, db: Session = Depends(get_db), current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return sip.new_sip(id, request, db)

@router.get('/{id}', response_model = List[schemas.ShowSIPPlan])
def show_one_sip_plan(id: int, db: Session = Depends(get_db), current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return sip.show_one_sip_plan(id, db)

@router.get('/', response_model = List[schemas.ShowSIPPlan])
def show_all_sip_plan(db: Session = Depends(get_db), current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return sip.show_all_sip_plan(db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_sip_plan(id: int, db: Session = Depends(get_db), current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return sip.delete_sip_plan(id, db)



@router.post('/{id}', response_model = schemas.ShowSIP)
def latest_sip_update(id: int, request: schemas.LatestSIP, db: Session = Depends(get_db), current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return sip.latest_sip_update(id, request, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def revert_latest_sip_transaction(id: int, db: Session = Depends(get_db), current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return sip.revert_latest_sip_transaction(id, db)

@router.get('/{id}', response_model = schemas.ShowSIP)
def latest_sip(id: int, db: Session = Depends(get_db), current_user: schemas.GetUser = Depends(oauth2.get_current_user)):
    return sip.latest_sip(id, db)