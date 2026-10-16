import redis.asyncio as aioredis
from app.core.config import settings

# Инициализируем асинхронный клиент Redis
redis_client = aioredis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
)