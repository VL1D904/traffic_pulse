from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from routes import pages, auth, video_api
from pathlib import Path
from security_token import SecurityToken
from repositories.video_source_repository import VideoSourceRepository
from repositories.admin_repository import AdminRepository
from source_handler import SourceHandler
from dotenv import load_dotenv
import asyncpg
import os
import asyncio


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await asyncpg.create_pool(
        database=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT"),
    )

    app.state.admin_repository = AdminRepository(app.state.pool)
    app.state.jwt_tokenizer = SecurityToken()
    app.state.video_source_repository = VideoSourceRepository(app.state.pool)
    app.state.source_handler = SourceHandler()

    try:
        await app.state.admin_repository.add_admin("admin", "admin")
    except Exception as e:
        print(f"\n[Lifespan Warning] Ошибка при добавлении администратора: {e}\n")


    yield

    if hasattr(app.state, "pool") and app.state.pool:
        print("[Lifespan] Закрытие пула соединений...")
        try:
            await asyncio.wait_for(app.state.pool.close(), timeout=2.0)
        except asyncio.TimeoutError:
            print(
                "[Lifespan] Пул завис при закрытии. Принудительное завершение (terminate)..."
            )
            app.state.pool.terminate()
        print("[Lifespan] Пул успешно закрыт.")

app = FastAPI(lifespan=lifespan)

app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(video_api.router)


