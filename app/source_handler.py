from dotenv import load_dotenv
import json
import redis
import os


load_dotenv()


class SourceHandler:
    def __init__(self):
        self.client = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            password=os.getenv("REDIS_PASSWORD"),
            decode_responses=True
        )
        self.channel = "video_commands"


    def publishing_source_notification(self, source_data: dict):
        source_json = json.dumps(source_data)
        self.client.publish(self.channel, source_json)