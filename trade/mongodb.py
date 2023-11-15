import motor.motor_asyncio
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field, EmailStr

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

print("Connecting to MongoDB...")
client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
database = client.trade
users = database.get_collection("users")
print("Connected to MongoDB!")


class UserBase(BaseModel):
    user_name: str = Field(..., unique=True,min_length=3, max_length=50)
    email: EmailStr = Field(..., unique=True)
    password: str = Field(..., unique=True)
    api_key_private: str = Field(..., unique=True)
    api_key_public: str = Field(..., unique=True)
    base_url: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str = Field(..., alias="_id")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "user_name": "johndoe",
                "email": "johndoe@example.com",
                "password": "secret",
                "api_key_private": "1234567890",
                "api_key_public": "0987654321",
                "base_url": "https://example.com",
            }
        }



def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "user_name": user["user_name"],
        "email": user["email"],
        "password": user["password"],
        "api_key_private": user["api_key_private"],
        "api_key_public": user["api_key_public"],
        "base_url": user["base_url"],
    }