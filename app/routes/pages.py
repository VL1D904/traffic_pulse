from fastapi import APIRouter, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from security_token import SecurityToken
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

router = APIRouter(tags=["Pages"])
router.mount("/static", StaticFiles(directory=BASE_DIR / 'static'), name="static")
templates = Jinja2Templates(directory=BASE_DIR / 'templates')

jwt_tokenizer = SecurityToken()

def get_current_user(request: Request) -> str | bool:
    session = request.cookies.get('admin_session', "")
    payload = jwt_tokenizer.decode_access_token(session) 
    if payload is None:
        return False
    return payload.get("login")

@router.get("/")
async def home_page(request: Request, user = Depends(get_current_user)):
    return templates.TemplateResponse(request=request,
                                        name="home.html",
                                        context={"user": user})