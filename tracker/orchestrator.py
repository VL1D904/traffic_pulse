from dotenv import load_dotenv
from video_worker import VideoWorker
import json
import redis
import os
import multiprocessing


load_dotenv()


class Orchestrator:
    def __init__(self) -> None:
        self.client = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            password=os.getenv("REDIS_PASSWORD"),
            decode_responses=True
        )
        self.channel = "video_commands"

        self.pubsub = self.client.pubsub()
        self.pubsub.subscribe(self.channel)

        self.processings = dict()

    def run_worker(self, url):
        worker = VideoWorker()
        worker.start(url)

    def listening(self) -> None:
        try:
            for message in self.pubsub.listen():
                if message["type"] != "message":
                    continue

                data = json.loads(message["data"])
                if data["command"] == "start":
                    process = multiprocessing.Process(target=self.run_worker, args=(data["url"], ))
                    self.processings[data["video_id"]] = process
                    process.start()
                    
                elif data["command"] == "stop":
                    process = self.processings.get(data["video_id"])
                    process.terminate()
        except KeyboardInterrupt:
            for process in self.processings.values():
                process.terminate()



if __name__ == "__main__":
    Orchestrator().listening()