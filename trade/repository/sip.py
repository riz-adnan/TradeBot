from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status

def new_sip(id: int, request: schemas.NewSIP, db: Session):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with the id {id} is not available")
    new_sip = models.sip_plan(sip_interval_amt = request.sip_interval_amt, sip_interval = request.sip_interval, sip_interval_days = request.sip_interval_days, start_date = request.start_date, user_id = id)
    db.add(new_sip)
    db.commit()
    db.refresh(new_sip)
    return new_sip

def show_one_sip_plan(id: int, db: Session):
    sip_plan = db.query(models.sip_plan).filter(models.sip_plan.user_id == id).all()
    if not sip_plan:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"sip plan with the id {id} is not available")
    return sip_plan

def show_all_sip_plan(db: Session):
    sip_plan = db.query(models.sip_plan).all()
    if not sip_plan:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"sip plan is not available")
    return sip_plan

def delete_sip_plan(id: int, db: Session):
    sip_plan = db.query(models.sip_plan).filter(models.sip_plan.sip_plan_id == id)
    if not sip_plan.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"sip plan with the id {id} is not available")
    sip_plan.delete(synchronize_session = False)
    db.commit()
    return 'done'

def latest_sip_update(id: int, request: schemas.LatestSIP, db: Session):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    sip_plan = db.query(models.sip_plan).filter(models.sip_plan.user_id == id and models.sip_plan.sip_interval_amt == request.sip_amt).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with the id {id} is not available")
    if not sip_plan:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"sip plan with the id {id} is not available")
    if request.sip_amt > user.balance:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = f"Insufficient balance")
    last_transaction = models.sip(date = request.date, sip_amt = request.sip_amt, total_bal = user.balance-request.sip_amt, fine = 0, next_pay = request.next_pay, user_id = id)
    db.add(last_transaction)
    db.commit()
    db.refresh(last_transaction)
    user.balance = user.balance - request.sip_amt
    db.commit()
    db.refresh(user)
    return last_transaction

def revert_latest_sip_transaction(id: int, db: Session):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    sip_plan = db.query(models.sip_plan).filter(models.sip_plan.user_id == id).all()
    last_transaction = db.query(models.SIP).filter(models.SIP.user_id == id).order_by(models.SIP.sip_id.desc()).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with the id {id} is not available")
    if not sip_plan:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"sip plan with the id {id} is not available")
    if not last_transaction:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Last transaction with the id {id} is not available")
    user.balance = user.balance + last_transaction.sip_amt
    db.commit()
    db.refresh(user)
    db.delete(last_transaction)
    db.commit()
    return 'done'

def latest_sip(id: int, db: Session):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    sip_plan = db.query(models.sip_plan).filter(models.sip_plan.user_id == id).all()
    last_transaction = db.query(models.SIP).filter(models.SIP.user_id == id).order_by(models.SIP.sip_id.desc()).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with the id {id} is not available")
    if not sip_plan:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"sip plan with the id {id} is not available")
    if not last_transaction:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Last transaction with the id {id} is not available")
    return last_transaction