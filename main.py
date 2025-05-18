from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import os

app = FastAPI()

# Статика
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/parking_spots.json")
async def get_parking_spots():
    return FileResponse("static/parking_spots.json")

# Путь к файлу статусов
status_file = "static/parking_status.json"

# Создание начального файла статусов
if not os.path.exists(status_file):
    with open("static/parking_spots.json") as f:
        spots = json.load(f)
    initial_status = {str(spot["id"]): "free" for spot in spots}
    with open(status_file, "w") as f:
        json.dump(initial_status, f)

# Модель обновления статуса
class StatusUpdate(BaseModel):
    id: str
    status: str  # "free" или "occupied"

@app.post("/update_status")
async def update_status(update: StatusUpdate):
    with open(status_file) as f:
        statuses = json.load(f)
    statuses[update.id] = update.status
    with open(status_file, "w") as f:
        json.dump(statuses, f)
    return {"result": "ok"}

# Эндпоинт /status — объединяет данные для карты
@app.get("/status")
async def get_combined_status():
    with open("static/parking_spots.json") as f:
        spots = json.load(f)
    with open(status_file) as f:
        statuses = json.load(f)

    combined = []
    for spot in spots:
        combined.append({
            "id": spot["id"],
            "lat": spot["lat"],
            "lon": spot["lon"],
            "zone": spot["zone"],
            "status": statuses.get(str(spot["id"]), "free")
        })
    return JSONResponse(content=combined)