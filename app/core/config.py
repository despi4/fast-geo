import redis.asyncio as aioredis
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

# Создаем приложение (аналог r := gin.Default())
app = FastAPI()

# Создаем асинхронное подключение к Redis
redis_client = aioredis.Redis(host="localhost", port=6379, decode_responses=True)


@app.get("/")
async def root():
  return {"message": "GeoPulse API работает!"}


# WebSocket эндпоинт (аналог обработки сокета в Go)
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
  await websocket.accept()
  print(f"Пользователь {user_id} подключился!")

  try:
    while True:
      # Ждем данные от клиента (например, {"lat": 55.75, "lon": 37.61})
      data = await websocket.receive_json()
      lat = data.get("lat")
      lon = data.get("lon")

      # Сохраняем в Redis через GEOADD
      await redis_client.geoadd("couriers", (lon, lat, user_id))

      # Ищем точки вокруг в радиусе 10 км
      nearby = await redis_client.geosearch(
          "couriers", longitude=lon, latitude=lat, radius=10, unit="km"
      )

      # Отправляем ответ обратно клиенту
      await websocket.send_json({"status": "ok", "nearby": nearby})

  except WebSocketDisconnect:
    print(f"Пользователь {user_id отключился}")
    await redis_client.zrem("couriers", user_id)