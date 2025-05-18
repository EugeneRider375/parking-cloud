from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI()

# CORS для доступа из любых источников (например, из браузера)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # можно ограничить конкретными адресами
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем статику
app.mount("/static", StaticFiles(directory="static"), name="static")

# Основная страница
@app.get("/")
def read_root():
    return FileResponse("static/index.html")

# Возвращает актуальный статус парковок
@app.get("/status")
def get_status():
    with open("static/parking_spots.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return JSONResponse(content=data)

# Приём обновлений статуса парковки
class ParkingStatus(BaseModel):
    id: str
    status: str

@app.post("/update_status")
async def update_status(data: ParkingStatus):
    file_path = "static/parking_spots.json"
    with open(file_path, "r", encoding="utf-8") as f:
        spots = json.load(f)
    for spot in spots:
        if spot["id"] == data.id:
            spot["status"] = data.status
            break
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(spots, f, indent=2, ensure_ascii=False)
    return {"message": f"Status updated for spot {data.id}"}
