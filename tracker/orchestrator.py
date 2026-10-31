from dotenv import load_dotenv
from video_worker import VideoWorker
import json
import redis
import os
import multiprocessing
import asyncio


load_dotenv()


# Класс оркестратор для управления воркерами трекинга видеопотока
class Orchestrator:
    def __init__(self) -> None:
        # Подключение к redis pubsub
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
        self.stop_events = dict()

    # Функция асинхронной запуска воркеров
    def run_worker(self, url: str, video_id: int ,stop_event: multiprocessing.Event) -> None:
        worker = VideoWorker(video_id, stop_event)
        asyncio.run(worker.start(url))

    # Функция создания процесса нового воркера
    def start_worker(self, url: str, video_id: int) -> None:
        stop_event = multiprocessing.Event()
        self.stop_events[video_id] = stop_event
        process = multiprocessing.Process(
            target=self.run_worker,
            args=(url, video_id, stop_event)
        )
        self.processings[video_id] = process
        process.start()
        print(f'Воркер {video_id} успешно запущен')

    # Функция безопасного завершения процесса воркера
    def stop_worker(self, video_id):
        stop_event: multiprocessing.Event = self.stop_events.get(video_id)
        process: multiprocessing.Process = self.processings.get(video_id)

        if not stop_event or not process:
            print(f'Воркер {video_id} не найден')
            return

        print(f'Отправляем сигнал остановки воркеру {video_id}')
        stop_event.set()

        process.join(timeout=10)

        if process.is_alive():
            print(f"Воркер {video_id} не закрылся за 5 секунд, принудительно вызываем SIGNTERM")
            process.terminate()
            process.join(2)

            if process.is_alive():
                print(f"Воркер {video_id} игнорирует SIGTERM, отправляем SIGKILL")
                process.kill()

        self.processings.pop(video_id)
        self.stop_events.pop(video_id)
        print(f"Воркер {video_id} полностью остановлен")

    # Функция прослушивания сообщений
    def listening(self) -> None:
        try:
            for message in self.pubsub.listen():
                if message["type"] != "message":
                    continue

                data = json.loads(message["data"])
                if data["command"] == "start":
                    self.start_worker(data["url"], data["video_id"])
                    
                elif data["command"] == "stop":
                    self.stop_worker(data["video_id"])
        except KeyboardInterrupt:
            keys = list(self.processings.keys())
            for video_id in keys:
                self.stop_worker(video_id)



if __name__ == "__main__":
    Orchestrator().listening()