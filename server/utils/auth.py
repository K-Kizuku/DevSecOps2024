import os
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.utils import formatdate
from random import randint

from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from jose import jwt
from sqlalchemy.orm.session import Session

from cruds.user import get_user_by_id, update_refresh_token
from db.database import get_db


TOKEN_SECRET = os.getenv("TOKEN_SECRET")
FROM_ADDRESS = os.environ.get("FROM_ADDRESS")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

security = HTTPBearer()

def create_one_time_tokens(db: Session, user_id: str, role: str):
    access_payload = {
        'token_type': 'access_token',
        'exp': datetime.utcnow() + timedelta(minutes=60),
        'user_id': user_id,
        'role': role
    }

    return jwt.encode(access_payload, TOKEN_SECRET, algorithm='HS256')

def create_tokens(db: Session, user_id: str, role: str):
    access_payload = {
        'token_type': 'access_token',
        'exp': datetime.utcnow() + timedelta(minutes=60),
        'user_id': user_id,
        'role': role
    }
    refresh_payload = {
        'token_type': 'refresh_token',
        'exp': datetime.utcnow() + timedelta(days=90),
        'user_id': user_id,
    }

    # トークン作成
    access_token = jwt.encode(access_payload, TOKEN_SECRET, algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload, TOKEN_SECRET, algorithm='HS256')

    if not update_refresh_token(db, user_id, refresh_token):
        raise HTTPException(status_code=400, detail="Failed to update refresh token.")

    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}

def get_current_user_from_token(db: Session, token: str, token_type: str):
    payload = jwt.decode(token, TOKEN_SECRET, algorithms=['HS256'])
    print(payload)
    if payload['token_type'] != token_type:
        raise HTTPException(status_code=401, detail=f'トークンタイプ不一致')

    user = get_user_by_id(db, payload['user_id'])

    # リフレッシュトークンの場合、受け取ったものとDBに保存されているものが一致するか確認
    if token_type == 'refresh_token' and user.refresh_token != token:
        print(user.refresh_token, '¥n', token)
        raise HTTPException(status_code=401, detail='リフレッシュトークン不一致')

    return user


credentials_exception = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    """アクセストークンからログイン中のユーザーを取得"""
    print(credentials)
    try:
        if credentials.scheme != 'Bearer':
            raise credentials_exception
        user = get_current_user_from_token(db, credentials.credentials, 'access_token')
    except Exception:
        raise credentials_exception
    return user

async def get_current_user_with_refresh_token(db: Session = Depends(get_db) ,credentials: HTTPAuthorizationCredentials = Security(security)):
    """リフレッシュトークンからログイン中のユーザーを取得"""
    print(credentials)
    try:
        if credentials.scheme != 'Bearer':
            print("called")
            raise credentials_exception
        user = get_current_user_from_token(db, credentials.credentials, 'access_token')
    except Exception:
        raise credentials_exception
    return user

def create_message(from_addr, to_addr, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()
    return msg

def send_mail(to_addr,body_msg,auth_num):
    smptobj = smtplib.SMTP('smtp.gmail.com',587)
    smptobj.ehlo()
    smptobj.starttls()
    smptobj.ehlo()
    smptobj.login(FROM_ADDRESS,MY_PASSWORD)
    smptobj.sendmail(FROM_ADDRESS,to_addr,f"{body_msg}{auth_num}")
    smptobj.close()

def create_auth_number():
    return str(randint(0,999999)).zfill(6)

