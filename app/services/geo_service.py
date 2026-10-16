from app.core.redis_client import redis_client

GEO_KEY = "active_couriers"


class GeoService:

  @staticmethod
  async def update_location(user_id: str, lat: float, lon: float):
    # Redis GEOADD принимает (ключ, долгота, широта, участник)
    await redis_client.geoadd(GEO_KEY, (lon, lat, user_id))

  @staticmethod
  async def find_nearby(lat: float, lon: float, radius: float = 5.0):
    # Ищем объекты в радиусе (в километрах)
    nearby = await redis_client.geosearch(
        GEO_KEY,
        longitude=lon,
        latitude=lat,
        radius=radius,
        unit="km",
        withdist=True,  # Вернуть также расстояние
    )
    return nearby

  @staticmethod
  async def remove_user(user_id: str):
    await redis_client.zrem(GEO_KEY, user_id)