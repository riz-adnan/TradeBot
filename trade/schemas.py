from pydantic import BaseModel
from typing import List, Optional

class GetUser(BaseModel):
    username: str
    email: str
    password: str
    api_key_private: str
    api_key_public: str
    base_url: str

class UpdateUser(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    api_key_private: Optional[str] = None
    api_key_public: Optional[str] = None
    base_url: Optional[str] = None

class ShowUser(BaseModel):
    user_name: str
    email: str
    class Config():
        orm_model = True

class UserDetails(BaseModel):
    user_name: str
    email: str
    api_key_private: str
    api_key_public: str
    base_url: str
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