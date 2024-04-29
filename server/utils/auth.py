import os
from datetime import datetime, timedelta
from random import randint

from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from jose import jwt
from sqlalchemy.orm.session import Session

from cruds.user import get_user_by_id
from db.database import get_db


TOKEN_SECRET = os.getenv("TOKEN_SECRET")

security = HTTPBearer()


def create_tokens(user_id: str, role: str):
    access_payload = {
        'token_type': 'access_token',
        'exp': datetime.utcnow() + timedelta(minutes=60*60*24),
        'user_id': user_id,
        'role': role
    }

    # トークン作成
    access_token = jwt.encode(access_payload, TOKEN_SECRET, algorithm='HS256')


    return {'access_token': access_token, 'token_type': 'bearer'}

def get_current_user_from_token(db: Session, token: str, token_type: str):
    payload = jwt.decode(token, TOKEN_SECRET, algorithms=['HS256'])
    print(payload)
    if payload['token_type'] != token_type:
        raise HTTPException(status_code=401, detail=f'トークンタイプ不一致')

    user = get_user_by_id(db, payload['user_id'])

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


