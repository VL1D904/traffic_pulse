from video_resolver import VideoResolver
from vk_video_resolver import VKVideoResolver
import re


# Фабричный класс для выбора типа VideoResolver по ссылки на видео
class VideoResolverFactory:
    @staticmethod
    def create(url: str) -> VideoResolver:
        # Проверка валидности url
        if not isinstance(url, str) or not url.startswith("http"):
            raise ValueError(f"Некорректный формат URL: {url}")

        # Определение домена url и выбор соответсвующего класса 
        if re.search(r"(vkvideo\.ru|vk\.ru|vk\.com)", url) is not None:
            return VKVideoResolver(url)
        else:
            raise ValueError(f"Неподдерживаемый тип источника для URL: {url}")