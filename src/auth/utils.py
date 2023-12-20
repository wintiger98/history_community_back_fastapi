from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from .schema import UserInput, UserUpdate, TokenData
from .models import User
from ..database import get_db
from ..config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# OAuth2PasswordBearer를 이용해 Bearer 토큰 받아오기
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
# password 암호화(bcrypt 암호화 알고리즘 이용)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta = None):
    """access_token 생성 메서드

    Args:
        data (dict): _description_
        expires_delta (timedelta, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(email: str, password: str, db: Session) -> User:
    """사용자 인증

    Args:
        email (str): _description_
        password (str): _description_
        db (Session): _description_

    Returns:
        User: _description_
    """
    user = get_user_by_email(email, db)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def verify_password(plain_password, hashed_password) -> bool:
    """들어온 비밀번호와 해시된 값(DB에 저장되어있음) 비교

    Args:
        plain_password (_type_): 들어온 비밀번호
        hashed_password (bool): DB에 저장되어있는 해시처리된 비밀번호

    Returns:
        _type_: _description_
    """
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(plain_password: str) -> str:
    """비밀번호 해싱

    Args:
        plain_password (str): _description_

    Returns:
        _type_: _description_
    """
    return pwd_context.hash(plain_password)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """인증이 필요한 엔드포인트에서 실행되는 함수.
    HTTP 요청에서 JWT 토큰을 읽어 사용자를 식별

    Args:
        token (str, optional): _description_. Defaults to Depends(oauth2_scheme).
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        credentials_exception: email이 없을 때
        credentials_exception: 토큰 해독 로직에 문제가 있을 때
        credentials_exception: email에 해당하는 유저가 없을 때

    Returns:
        User: _description_
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 토큰 해독 -> 페이로드 추출
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = get_user_by_email(email=token_data.email, db=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


def get_user_by_email(email: str, db: Session) -> User:
    """email로 user 찾기

    Args:
        email (str): _description_
        db (Session): _description_

    Returns:
        User: _description_
    """
    stmt = select(User).where(User.email == email)
    result = db.execute(stmt)
    user = result.scalar()
    return user


def create_user(data: UserInput, db: Session) -> User:
    """사용자 생성
    1. 비밀번호 해시
    2. 사용자 생성
    3. 사용자 저장
    4. 사용자 반환

    Args:
        data (dict): _description_
        db (Session): _description_

    Returns:
        User: _description_
    """
    # 비밀번호 해시
    data.password = hash_password(data.password)

    # 사용자 생성
    new_user = User(**data.model_dump())

    # 사용자 저장
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def update_user(data: UserUpdate, user: User, db: Session) -> dict:
    """사용자 수정

    Args:
        data (UserUpdate): _description_
        user (User): _description_
        db (Session): _description_

    Returns:
        User: _description_
    """

    # 비밀번호 해시
    try:
        if data.password:
            data.password = hash_password(data.password)
    except:
        return {"result": False, "detail": "Password hash failed"}

    # 수정
    try:
        for key, value in data.model_dump().items():
            setattr(user, key, value)
    except:
        return {"result": False, "detail": "data update failed"}

    try:
        db.commit()
    except:
        return {"result": False, "detail": "database commit failed"}
    return {"result": True}


def delete_user(user: User, db: Session) -> dict:
    """사용자 삭제

    Args:
        user (User): _description_
        db (Session): _description_

    Returns:
        dict: _description_
    """
    try:
        db.delete(user)
        db.commit()

        return True
    except:
        return False
