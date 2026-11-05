from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates
from pathlib import Path
from repositories.admin_repository import AdminRepository
from security_token import SecurityToken
from repositories.video_source_repository import VideoSourceRepository
from source_handler import SourceHandler


BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / 'templates')

def get_video_source_repository(request: Request) -> VideoSourceRepository:
    return request.app.state.video_source_repository

def get_admin_repository(request: Request) -> AdminRepository:
    return request.app.state.admin_repository

def get_source_handler(request: Request) -> SourceHandler:
    return request.app.state.source_handler

def get_jwt_tokenizer(request: Request) -> SecurityToken:
    return request.app.state.jwt_tokenizer


def get_current_user(request: Request, jwt_tokenizer: SecurityToken = Depends(get_jwt_tokenizer)) -> str | bool:
    session = request.cookies.get('admin_session', "")
    payload = jwt_tokenizer.decode_access_token(session) 
    if payload is None:
        return False
    return payload.get("login")