from enum import Enum

from pydantic import BaseModel


class Role(str, Enum):
    admin = "admin"
    user = "user"

class User(BaseModel):
    id: str
    municipality: str
    email: str
    role: Role

    class Config:
        from_attributes = True

class LoginUserPayload(BaseModel):
    email: str
    password: str

class RegisterUserPayload(BaseModel):
    email: str
    password: str
    municipality: str

class SecondaryAuthUserPayload(BaseModel):
    code:str