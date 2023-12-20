from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth.router import router as auth_router
from .auth.models import User
from .countries.models import Country, Cheer
from .countries.posts.models import Post, PostLikeDislike
from .countries.posts.replies.models import Reply, ReplyLikeDislike
from .mappers.models import user_country_mapper

app = FastAPI()
app.include_router(auth_router)

# CORS 설정 추가
origins = [
    "http://localhost:8080",
    "http://localhost:8081",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8081",
]  # 허용할 출처를 여기에 추가

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}
