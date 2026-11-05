from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from routes import pages, auth, video_api
from pathlib import Path
from security_token import SecurityToken
from repositories.video_source_repository import VideoSourceRepository
from repositories.admin_repository import AdminRepository
from source_handler import SourceHandler


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.admin_repository = AdminRepository()
    app.state.admin_repository.add_admin("admin", "admin")
    app.state.jwt_tokenizer = SecurityToken()
    app.state.video_source_repository = VideoSourceRepository()
    app.state.source_handler = SourceHandler()

    try:
        app.state.admin_repository.add_admin("admin", "admin")
    except Exception as e:
        print(f"\n[Lifespan Warning] Ошибка при добавлении администратора: {e}\n")


    yield

    app.state.admin_repository.close()
    app.state.video_source_repository.close()

app = FastAPI(lifespan=lifespan)

app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(video_api.router)


