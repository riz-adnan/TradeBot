from pydantic import BaseModel
from typing import List, Optional

class GetUser(BaseModel):
    username: str
    email: str
    password: str
    api_key_private: str
    api_key_public: str
    base_url: str
    # balance: float

class UpdateUser(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    api_key_private: Optional[str] = None
    api_key_public: Optional[str] = None
    base_url: Optional[str] = None

# class UpdateInvestment(BaseModel):
#     date: str
#     invested_amt: float

# class ShowInvestment(BaseModel):
#     date: str
#     invested: float
#     class Config():
#         orm_model = True

# class LatestSIP(BaseModel):
#     date: str
#     sip_amt: float
#     next_pay: str

# class ShowSIP(BaseModel):
#     date: str
#     sip_amt: float
#     fine: float
#     next_pay: str
#     class Config():
#         orm_model = True

# class LatestSOP(BaseModel):
#     date: str
#     sop_amt: float
#     next_pay: str

# class ShowSOP(BaseModel):
#     date: str
#     sop_amt: float
#     # fine: float
#     next_pay: str
#     class Config():
#         orm_model = True

# class NewSIP(BaseModel):
#     sip_interval_amt: float
#     sip_interval: str
#     sip_interval_days: int
#     start_date: str

# class ShowSIPPlan(BaseModel):
#     sip_interval_amt: float
#     sip_interval: str
#     sip_interval_days: int
#     start_date: str
#     class Config():
#         orm_model = True

# class NewSOP(BaseModel):
#     sop_interval_amt: float
#     sop_interval: str
#     sop_interval_days: int
#     start_date: str

# class ShowSOPPlan(BaseModel):
#     sop_interval_amt: float
#     sop_interval: str
#     sop_interval_days: int
#     start_date: str
#     class Config():
#         orm_model = True

class ShowUser(BaseModel):
    user_name: str
    email: str
    # balance: float
    # profit: float
    # invested_amt: float
    # acc_fine: float
    # sip_plans: List[ShowSIPPlan] = []
    # sop_plans: List[ShowSOPPlan] = []
    class Config():
        orm_model = True

class UserDetails(BaseModel):
    user_name: str
    email: str
    api_key_private: str
    api_key_public: str
    base_url: str
    # balance: float
    # profit: float
    # invested_amt: float
    # acc_fine: float
    # sip_plan: List[ShowSIPPlan] = []
    # sop_plan: List[ShowSOPPlan] = []
    # investments: List[ShowInvestment] = []
    class Config():
        orm_model = True


class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None