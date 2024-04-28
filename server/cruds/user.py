import os

import bcrypt
from fastapi import HTTPException
from sqlalchemy.orm.session import Session

from db.models import User
from schema.user import User as UserSchema

salt = os.environ.get('PASSWORD_HASH_SALT',
                      '$2a$10$ThXfVCPWwXYx69U8vuxSUu').encode()

def gen_password_hash(password: str):
    hash = bcrypt.hashpw(password.encode(), salt)
    return hash.decode()

def authenticate(db, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    password_hash = gen_password_hash(password)
    if user.password_hash != password_hash:
        raise HTTPException(status_code=401, detail="Incorrect password")
    return user

def update_refresh_token(db: Session, user_id: str, refresh_token: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.refresh_token = refresh_token
    db.add(user)
    db.commit()
    return True

def get_user_by_id(db: Session, user_id: str) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def create_new_user(db: Session, email: str, password: str,municipality: str) -> User:
    user = User(email=email, password_hash=gen_password_hash(password), municipality=municipality)
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserSchema.from_orm(user)

def register_auth_number(db:Session,auth_number:str,email:str):
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    auth_hash_num = gen_password_hash(auth_number)
    user.auth_hash_num = auth_hash_num
    # db.add(user)
    db.commit()
    return True

