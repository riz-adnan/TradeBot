from sqlalchemy import Column, Integer, String, ForeignKey, Float, ARRAY
from .database import Base
# from sqlalchemy.orm import relationship

# class sip_plan(Base):
#     __tablename__ = 'sip_plan'
#     sip_plan_id = Column(Integer, primary_key = True, index = True)
#     sip_interval_amt = Column(Float)
#     sip_interval = Column(String)
#     sip_interval_days = Column(Integer)
#     start_date = Column(String)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     customer = relationship("Users", back_populates="sip_plans")

# class sop_plan(Base):
#     __tablename__ = 'sop_plan'
#     sop_plan_id = Column(Integer, primary_key = True, index = True)
#     sop_interval_amt = Column(Float)
#     sop_interval = Column(String)
#     sop_interval_days = Column(Integer)
#     start_date = Column(String)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     customer = relationship("Users", back_populates="sop_plans")

# class Investment(Base):
#     __tablename__ = 'investment'
#     invst_id = Column(Integer, primary_key = True, index = True)
#     date = Column(String)
#     invested = Column(Float)
#     total_bal = Column(Float)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     customer = relationship("Users", back_populates="investments")

# class SIP(Base):
#     __tablename__ = 'sip'
#     sip_id = Column(Integer, primary_key = True, index = True)
#     date = Column(String)
#     sip_amt = Column(Float)
#     total_bal = Column(Float)
#     fine = Column(Float)
#     next_pay = Column(String)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     customer = relationship("Users", back_populates="sips")

# class SOP(Base):
#     __tablename__ = 'sop'
#     sop_id = Column(Integer, primary_key = True, index = True)
#     date = Column(String)
#     sop_amt = Column(Float)
#     total_bal = Column(Float)
#     # fine = Column(Float)
#     next_pay = Column(String)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     customer = relationship("Users", back_populates="sops")

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True, index = True)
    user_name = Column(String)
    email = Column(String)
    password = Column(String)
    api_key_private = Column(String)
    api_key_public = Column(String)
    base_url = Column(String)
    # balance = Column(Float)
    # profit = Column(Float)
    # invested_amt = Column(Float)
    # acc_fine = Column(Float)
    # investments = relationship("Investment", back_populates="customer")
    # sips = relationship("SIP", back_populates="customer")
    # sops = relationship("SOP", back_populates="customer")
    # sip_plans = relationship("sip_plan", back_populates="customer")
    # sop_plans = relationship("sop_plan", back_populates="customer")