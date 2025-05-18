from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Отдаём HTML и JS из папки "static"
app.mount("/", StaticFiles(directory="static", html=True), name="static")