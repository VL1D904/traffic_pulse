from fastapi import APIRouter, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.dependencies import BASE_DIR, templates, get_current_user, video_source_repository



router = APIRouter(tags=["Pages"])
router.mount("/static", StaticFiles(directory=BASE_DIR / 'static'), name="static")

@router.get("/")
async def home_page(request: Request, user = Depends(get_current_user)):
    sources = video_source_repository.get_video_sources()
    return templates.TemplateResponse(request=request,
                                        name="home.html",
                                        context={"user": user, "sources": sources})

@router.get("/{source_id}")
async def source_page(request: Request, source_id: int, user = Depends(get_current_user)):
    source_info = video_source_repository.get_video_sources(source_id)
    return templates.TemplateResponse(request=request,
                                        name="source.html",
                                        context={"source_info": source_info, "user": user, "source_id": source_id})