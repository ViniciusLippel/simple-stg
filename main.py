from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

PHOTOS_DIR = Path("photos")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

app = FastAPI()

app.mount("/photos", StaticFiles(directory=PHOTOS_DIR), name="photos")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.get("/api/folders")
def list_folders():
    if not PHOTOS_DIR.exists():
        return []
    folders = sorted(
        d.name for d in PHOTOS_DIR.iterdir() if d.is_dir()
    )
    return folders


@app.get("/api/photos/{folder}")
def list_photos(folder: str):
    folder_path = PHOTOS_DIR / folder
    if not folder_path.exists() or not folder_path.is_dir():
        raise HTTPException(status_code=404, detail="Folder not found")
    photos = sorted(
        f.name
        for f in folder_path.iterdir()
        if f.is_file() and f.suffix.lower() in ALLOWED_EXTENSIONS
    )
    return photos
