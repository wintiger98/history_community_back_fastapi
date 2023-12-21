from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.main import app
from src.database import Base
from src.database import get_db

# 테스트 데이터베이스 따로 생성
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """FastAPI 애플리케이션에서 get_db 함수가 호출될 때마다 override_get_db 함수를 대신 호출하도록 설정

    Yields:
        _type_: _description_
    """
    db = None
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# 기존 get_db 오버라이딩해서 사용
app.dependency_overrides[get_db] = override_get_db


def setup_function(function):
    # 테스트 데이터베이스 초기화
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


client = TestClient(app)
