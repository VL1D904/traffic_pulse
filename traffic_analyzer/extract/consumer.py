from dotenv import load_dotenv
import os
import aiokafka
import asyncio
import json


load_dotenv()


class Consumer:
    def __init__(self):
        self.bootstrap_server = os.getenv("KAFKA_BOOTSTRAP_SERVER")
        self.topic = os.getenv("KAFKA_TOPIC")
        self.consumer = aiokafka.AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_server
        )

    async def start(self):
        await self.consumer.start()

    async def stop(self):
        await self.consumer.stop()

    async def listening(self):
        try:
            async for message in self.consumer:
                data = json.loads(message.value.decode('utf-8'))
                yield data
        except (json.JSONDecodeError, UnicodeDecodeError) as ex:
            print(f"Ошибка десериализации: {ex}")
        finally:
            await self.stop()