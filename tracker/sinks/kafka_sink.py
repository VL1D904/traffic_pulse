from sinks.base_sink import BaseSink
from contracts.frame_result_contract import FrameResultContract
from detection_preprocessing import DetectionPreprocessing
from aiokafka import AIOKafkaProducer
from dotenv import load_dotenv
from typing import Optional
import os
import json


load_dotenv()


class KafkaSink(BaseSink):
    def __init__(self) -> None:
        self.bootstrap_server = os.getenv("KAFKA_BOOTSTRAP_SERVER")
        self.topic = os.getenv("KAFKA_TOPIC")
        self.producer: Optional[AIOKafkaProducer] = None

    async def connect(self) -> None:
        if self.producer is not None:
            return

        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_server,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: str(k).encode('utf-8') if k is not None else None
        )

        await self.producer.start()

    async def close(self) -> None:
        if self.producer:
            await self.producer.stop()

    async def send(self, frame_result: FrameResultContract, video_id: int) -> None:
        if not self.producer:
            raise RuntimeError("Kafka не подключена")

        detections = DetectionPreprocessing.preprocess(video_id, frame_result)

        if not detections:
            return

        await self.producer.send_and_wait(
            topic=self.topic,
            value=detections,
            key=video_id
        )

