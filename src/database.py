from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1111@host.docker.internal/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL, client_encoding="utf8")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
