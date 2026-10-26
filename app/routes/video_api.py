from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from dependies import BASE_DIR, templates, video_source_repository, get_current_user, source_handler
from video_source import VideoSource
from worker_structure import WorkerStructure


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

@router.put("/start_worker")
async def start_worker(worker_structure: WorkerStructure):
    try:
        video_source = video_source_repository.get_video_sources(worker_structure.video_id)
        video_source_dict = {
            "video_id": video_source[0],
            "command": "start",
            "url": video_source[4]
        }
        source_handler.publishing_source_notification(video_source_dict)
        return JSONResponse({"message": "Сообщение о запуске воркера успешно отправлено"})
    except Exception as ex:
        return JSONResponse({"message": f"Произошла ошибка: {ex}"})


@router.delete("/stop_worker")
async def stop_worker(worker_structure: WorkerStructure):
    try:
        video_source = video_source_repository.get_video_sources(worker_structure.video_id)
        video_source_dict = {
            "video_id": video_source[0],
            "command": "stop",
            "url": video_source[4]
        }
        source_handler.publishing_source_notification(video_source_dict)
        return JSONResponse({"message": "Сообщение о запуске воркера успешно отправлено"})
    except Exception as ex:
        return JSONResponse({"message": f"Произошла ошибка: {ex}"})