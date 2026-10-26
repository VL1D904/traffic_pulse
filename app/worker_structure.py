from pydantic import BaseModel


class WorkerStructure(BaseModel):
    video_id: int