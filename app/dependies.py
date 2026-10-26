from fastapi import Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from admin import AdminModel
from security_token import SecurityToken
from video_source_repository import VideoSourceRepository
from source_handler import SourceHandler


BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / 'templates')


admin_model = AdminModel()
admin_model.add_admin("admin", "admin")

jwt_tokenizer = SecurityToken()

video_source_repository = VideoSourceRepository()

source_handler = SourceHandler()

def get_current_user(request: Request) -> str | bool:
    session = request.cookies.get('admin_session', "")
    payload = jwt_tokenizer.decode_access_token(session) 
    if payload is None:
        return False
    return payload.get("login")