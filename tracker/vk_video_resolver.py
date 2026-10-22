from video_resolver import VideoResolver
from typing import Generator
import time
import os
import subprocess
import numpy as np


# Класс для чтения видеопотока с платформы VK
class VKVideoResolver(VideoResolver):
    def __init__(self, video_url: str) -> None:
        super().__init__(video_url)

        # Констатные переменные для работы с видеопотоком
        self.COOKIE_FILE = './opt/vk_cookies.txt'
        self.COOKIE_TTL = 60 * 60
        self.WIDTH = 1920
        self.HEIGHT = 1080
        self.CHANNELS = 3
        self.FFMPEG_TTL = 60

        # Команды для получения url видеопотока в формате .m3u8 и экспорта куки из vk
        self.stream_url = ""
        self.yt_dlp_command = ["yt-dlp", "--cookies", self.COOKIE_FILE, '--get-url', '-v', self.video_url]
        self.export_cookie_command = ["yt-dlp",
                                      "--cookies-from-browser", "firefox",
                                      "--cookies", self.COOKIE_FILE,
                                      "https://vk.com",
                                      "--no-download"]

        self.ffmpeg_process = None

    # Функция получения ссылки видеопотока .m3u8
    def resolve_stream(self) -> None:
        try:
            # Загрузка и обновление куки vk
            current_time = time.time()
            if not os.path.exists(self.COOKIE_FILE) or (current_time - os.path.getatime(self.COOKIE_FILE)) > self.COOKIE_TTL:
                subprocess.run(self.export_cookie_command)

            # Получение ссылки
            process = subprocess.run(self.yt_dlp_command, check=True, capture_output=True, text=True)
            self.stream_url = process.stdout.strip()
        except subprocess.CalledProcessError as err:
            print(f"Произошла ошибка получения url потока:\n{err.stderr}")

    # Функция запуска процесса чтения кадров видеопотока через ffmpeg
    def ffmpeg_reader(self) -> None:
        ffmpeg_command = ["ffmpeg",
                            "-user_agent", "AppleWebKit/537.36 Chrome/120.0.0.0",
                            "-referer", "https://vkvideo.ru",
                            "-i", self.stream_url,
                            "-f", "rawvideo",
                            "-s", f"{self.WIDTH}x{self.HEIGHT}",
                            "-pix_fmt", "bgr24",
                            "-r", "15",
                            "pipe:1"]

        self.ffmpeg_process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Функция остановки процесса ffmpeg
    def stop_ffmpeg(self) -> None:
        if self.ffmpeg_process is None:
            return

        self.ffmpeg_process.terminate()
        try:
            self.ffmpeg_process.wait(5)
        except subprocess.TimeoutExpired:
            self.ffmpeg_process.kill()
            try:
               self.ffmpeg_process.wait(5)
            except subprocess.TimeoutExpired:
                print("Процесс умер") 

    # Функция получения кадров видеопотока
    def get_frames(self) -> Generator:
        try:
            self.resolve_stream()
            self.ffmpeg_reader()

            start_time = time.time()
            frame_count = 0

            while True:
                # Обновление ffmpeg процесса
                current_time = time.time()
                if current_time - start_time >= self.FFMPEG_TTL:
                    self.stop_ffmpeg()
                    self.resolve_stream()
                    self.ffmpeg_reader()
                    start_time = time.time()

                # Чтение и преобразование кадров видеопотока
                raw_frame = self.ffmpeg_process.stdout.read(self.WIDTH * self.HEIGHT * self.CHANNELS)
                frame_count += 1
                if len(raw_frame) != self.WIDTH * self.HEIGHT * self.CHANNELS:
                    continue

                frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((self.HEIGHT, self.WIDTH, self.CHANNELS))

                yield (frame, frame_count)
        except Exception as ex:
            print(f"Произошла ошибка {ex}")
        finally:
            self.stop_ffmpeg()