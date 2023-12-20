from fastapi import APIRouter, HTTPException, Depends, Form, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from .utils import (
    authenticate_user,
    create_access_token,
    delete_user,
    get_current_user,
    get_user_by_email,
    create_user,
    update_user,
)
from .models import User
from .schema import UserOutput, Token, UserInput, UserUpdate

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """로그인 함수
    1. OAuth2 객체를 이용해 요청에서 사용자 이름(여기선 email), 비밀번호 받기
    2. authenticate_user 함수로 사용자 검증 -> 실패시 401
    3. create_access_token 함수로 JWT 토큰 발급
    4. 응답에 토큰 반환

    Args:
        form_data (OAuth2PasswordRequestForm, optional): _description_. Defaults to Depends().
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: 401

    Returns:
        _type_: _description_
    """
    user = await authenticate_user(
        email=form_data.username, password=form_data.password, db=db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=UserOutput)
async def user_register(user_data: UserInput, db: Session = Depends(get_db)):
    """회원가입
    1. 사용자 중복 확인
    2. 사용자 생성
    3. 사용자 반환

    Args:
        user_data (UserInput): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    user = get_user_by_email(email=user_data.email, db=db)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(user_data, db=db)
    return user


@router.get("/me", response_model=UserOutput)
async def read_me(user: User = Depends(get_current_user)):
    """토큰을 이용해 사용자 정보 확인

    Args:
        user (User, optional): _description_. Defaults to Depends(get_current_user).

    Returns:
        _type_: _description_
    """
    return user


@router.put("/me", response_model=dict)
async def change_user(
    data: UserUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """사용자 수정

    Args:
        data (UserUpdate): _description_
        user (User, optional): _description_. Defaults to Depends(get_current_user).
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    result = update_user(data=data, user=user, db=db)
    if result["result"]:
        return {"detail": "User updated"}
    else:
        raise HTTPException(status_code=400, detail=result["detail"])


@router.delete("/me", response_model=dict)
async def erase_user(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """사용자 삭제

    Args:
        user (User, optional): _description_. Defaults to Depends(get_current_user).
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    if delete_user(user=user, db=db):
        return {"detail": "User deleted"}
    else:
        raise HTTPException(status_code=400, detail="User delete failed")
