from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status
from ..hashing import Hash

def new_investment(id: int, request: schemas.UpdateInvestment, db: Session):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with the id {id} is not available")
    if request.invested_amt > user.balance:
        raise HTTPException(status_code = status.HTTP_406_NOT_ACCEPTABLE, detail = f"Insufficient balance")
    new_investment = models.Investment(date = request.date, invested = request.invested_amt, total_bal = user.balance-request.invested_amt, user_id = id)
    db.add(new_investment)
    db.commit()
    db.refresh(new_investment)
    user.balance = user.balance - request.invested_amt
    db.commit()
    db.refresh(user)
    return new_investment

def show_ones_investment(id: int, db: Session):
    user = db.query(models.Users).filter(models.Users.id == id)
    if not user.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with the id {id} is not available")
    return db.query(models.Investment).filter(models.Investment.user_id == id).all()

def show_all_investment(db: Session):
    return db.query(models.Investment).all()

def revert_latest_investment(id: int, db: Session):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    investment = db.query(models.Investment).filter(models.Investment.user_id == id).all()
    last_transaction = db.query(models.Investment).filter(models.Investment.user_id == id).order_by(models.Investment.invst_id.desc()).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with the id {id} is not available")
    if not investment:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Investment with the id {id} is not available")
    user.balance = user.balance + last_transaction.invested
    db.commit()
    db.refresh(user)
    last_transaction.delete(synchronize_session = False)
    db.commit()
    return last_transaction