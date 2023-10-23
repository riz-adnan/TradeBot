from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status

def new_sop(id: int, request: schemas.NewSOP, db: Session):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with the id {id} is not available")
    new_sop = models.sop_plan(sop_interval_amt = request.sop_interval_amt, sop_interval = request.sop_interval, sop_interval_days = request.sop_interval_days, start_date = request.start_date, user_id = id)
    db.add(new_sop)
    db.commit()
    db.refresh(new_sop)
    return new_sop

def show_one_sop_plan(id: int, db: Session):
    sop_plan = db.query(models.sop_plan).filter(models.sop_plan.user_id == id).all()
    if not sop_plan:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"SOP plan with the id {id} is not available")
    return sop_plan

def show_all_sop_plan(db: Session):
    sop_plan = db.query(models.sop_plan).all()
    if not sop_plan:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"SOP plan is not available")
    return sop_plan

def delete_sop_plan(id: int, db: Session):
    sop_plan = db.query(models.sop_plan).filter(models.sop_plan.sop_plan_id == id)
    if not sop_plan.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"SOP plan with the id {id} is not available")
    sop_plan.delete(synchronize_session = False)
    db.commit()
    return 'done'

def latest_sop_update(id: int, request: schemas.LatestSOP, db: Session):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    sop_plan = db.query(models.sop_plan).filter(models.sop_plan.user_id == id and models.sop_plan.sop_interval_amt == request.sop_amt).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with the id {id} is not available")
    if not sop_plan:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"SOP plan with the id {id} is not available")
    # if request.sop_amt > user.balance:
    #     raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = f"Insufficient balance")
    last_transaction = models.SOP(date = request.date, sop_amt = request.sop_amt, total_bal = user.balance+request.sop_amt, next_pay = request.next_pay, user_id = id)
    db.add(last_transaction)
    db.commit()
    db.refresh(last_transaction)
    user.balance = user.balance - request.sop_amt
    db.commit()
    db.refresh(user)
    return last_transaction

def revert_latest_sop_transaction(id: int, db: Session):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    sop_plan = db.query(models.sop_plan).filter(models.sop_plan.user_id == id).all()
    last_transaction = db.query(models.SOP).filter(models.SOP.user_id == id).order_by(models.SOP.sop_id.desc()).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with the id {id} is not available")
    if not sop_plan:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"SOP plan with the id {id} is not available")
    if not last_transaction:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Last transaction with the id {id} is not available")
    user.balance = user.balance - last_transaction.sop_amt
    db.commit()
    db.refresh(user)
    db.delete(last_transaction)
    db.commit()
    return 'done'

def latest_sop(id: int, db: Session):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    sop_plan = db.query(models.sop_plan).filter(models.sop_plan.user_id == id).all()
    last_transaction = db.query(models.SOP).filter(models.SOP.user_id == id).order_by(models.SOP.sop_id.desc()).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with the id {id} is not available")
    if not sop_plan:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"SOP plan with the id {id} is not available")
    if not last_transaction:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Last transaction with the id {id} is not available")
    return last_transaction