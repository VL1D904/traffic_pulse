from fastapi import APIRouter, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from dependencies import BASE_DIR, templates, get_admin_repository, get_jwt_tokenizer
from repositories.admin_repository import AdminRepository
from security_token import SecurityToken



router = APIRouter(prefix='/auth', tags=["Auth"])
router.mount("/static", StaticFiles(directory=BASE_DIR / 'static'), name="static")


@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(request=request,
                                          name="login.html",
                                          context={"user_exist": True})

@router.post("/login")
async def login_admin(
    request: Request,
    login = Form(), 
    password = Form(),
    admin_model: AdminRepository = Depends(get_admin_repository),
    jwt_tokenizer: SecurityToken = Depends(get_jwt_tokenizer)
    ):
    is_admin = admin_model.check_admin(login, password)
    if not is_admin:
        return templates.TemplateResponse(request=request,
                                          name="login.html",
                                          context={"user_exist": False})

    user_data = {"login": login}
    jwt_token = jwt_tokenizer.create_access_token(user_data)
    response = RedirectResponse('/', status_code=302)
    response.set_cookie(
        key="admin_session",
        value=jwt_token,
        httponly=True,
        secure=False,
        max_age=1800
    )
    return response

@router.post("/logout")
async def logout(request: Request):
    response = RedirectResponse('/', status_code=302)
    response.delete_cookie(key="admin_session")
    return response