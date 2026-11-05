from enum import Enum


class VideoStatus(Enum):
    INACTIVE = "inactive"
    ACTIVE = "active"
    PENDING = "pending"
    ERROR = "error"
    COMPLETED = "completed"
    CANCELED = "canceled"