from pydantic import BaseModel


class VideoSource(BaseModel):
    city: str
    street: str
    url: str