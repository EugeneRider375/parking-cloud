from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import os

app = FastAPI()

# Папка со статикой
app.mount("/static", StaticFiles(directory="static"), name="static")

# Основная страница
@app.get("/")
async def root():
    return FileResponse("static/index.html")

# Отдаём JSON с парковками
@app.get("/parking_spots.json")
async def get_parking_spots():
    return FileResponse("static/parking_spots.json")

# ====== Хранилище статусов ======
status_file = "static/parking_status.json"

# Если файла нет — создаём пустые статусы
if not os.path.exists(status_file):
    with open("static/parking_spots.json") as f:
        spots = json.load(f)
    initial = {spot["id"]: "free" for spot in spots}
    with open(status_file, "w") as f:
        json.dump(initial, f)

# ==== Получить текущий статус ====
@app.get("/get_status")
async def get_status():
    with open(status_file) as f:
        return JSONResponse(content=json.load(f))

# ==== Обновить статус ====
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
