from fastapi import FastAPI
from app.api.v1.websockets import router as ws_router

app = FastAPI(title="GeoPulse API", version="1.0.0")

# Подключаем роутеры
app.include_router(ws_router, prefix="/api/v1")


@app.get("/")
async def root():
  return {"message": "GeoPulse API успешно запущен!"}