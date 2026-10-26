from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from dependies import BASE_DIR, templates, video_source_repository, get_current_user
from video_source import VideoSource


router = APIRouter(prefix="/video_api", tags=["Video API"])
router.mount("/static", StaticFiles(directory=BASE_DIR / 'static'), name="static")


@router.post("/add_source")
async def add_source(video_source: VideoSource, user = Depends(get_current_user)):
    if user is None:
        return JSONResponse({"message": "Отсутсвуют права доступа к добавлению источника"}, 403)
    is_source = video_source_repository.check_source_exists(video_source.url)
    if is_source:
        return JSONResponse({"message": "Источник уже существует"}, 409)

    video_source_repository.insert_video_source(video_source)
    response = RedirectResponse('/', status_code=302)
    return response

@router.get("/video_status")
async def get_video_status(video_id: int):
    video_status = video_source_repository.get_video_sources()[0][1]
    if video_status is None:
        return JSONResponse({"message": "Трансляция не найдена"}, 404)
    return JSONResponse({"status": video_status}, 200) 