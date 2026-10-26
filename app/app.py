from fastapi import FastAPI, Request
from routes import pages, auth, video_api
from pathlib import Path


app = FastAPI()

app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(video_api.router)


