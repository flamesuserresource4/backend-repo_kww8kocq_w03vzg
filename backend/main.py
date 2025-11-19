from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database import create_document, get_documents, update_document, delete_document
from schemas import Notice, Event, Faculty, Department, Admission, GalleryImage

app = FastAPI(title="Emel Laboratory School & Arojbegi Laboratory College API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

# Simple in-memory admin credential for demo
ADMIN_USER = {"username": "admin", "password": "admin123"}

@app.post("/admin/login")
async def admin_login(payload: LoginRequest):
    if payload.username == ADMIN_USER["username"] and payload.password == ADMIN_USER["password"]:
        return {"token": "demo-token", "user": {"name": "Administrator"}}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/info")
async def info():
    return {
        "school": {
            "name": "Emel Laboratory School",
            "code": "484281",
            "emis": "00505030438",
        },
        "college": {
            "name": "Arojbegi Laboratory College",
            "eiin": "139583",
        },
        "message": "Welcome to our combined institution API"
    }

# Notices
@app.post("/notices", response_model=dict)
async def create_notice(notice: Notice):
    _id = await create_document("notice", notice.model_dump(by_alias=True, exclude_none=True))
    return {"id": _id}

@app.get("/notices")
async def list_notices(audience: Optional[str] = None, limit: int = 50):
    filter_dict = {"audience": audience} if audience else None
    docs = await get_documents("notice", filter_dict, limit)
    return docs

# Events
@app.post("/events", response_model=dict)
async def create_event(event: Event):
    _id = await create_document("event", event.model_dump(by_alias=True, exclude_none=True))
    return {"id": _id}

@app.get("/events")
async def list_events(audience: Optional[str] = None, limit: int = 50):
    filter_dict = {"audience": audience} if audience else None
    docs = await get_documents("event", filter_dict, limit)
    return docs

# Faculty
@app.post("/faculty", response_model=dict)
async def create_faculty(member: Faculty):
    _id = await create_document("faculty", member.model_dump(by_alias=True, exclude_none=True))
    return {"id": _id}

@app.get("/faculty")
async def list_faculty(level: Optional[str] = None, department: Optional[str] = None, limit: int = 100):
    filter_dict = {}
    if level:
        filter_dict["level"] = level
    if department:
        filter_dict["department"] = department
    docs = await get_documents("faculty", filter_dict or None, limit)
    return docs

# Departments
@app.post("/departments", response_model=dict)
async def create_department(dep: Department):
    _id = await create_document("department", dep.model_dump(by_alias=True, exclude_none=True))
    return {"id": _id}

@app.get("/departments")
async def list_departments(level: Optional[str] = None, limit: int = 100):
    filter_dict = {"level": level} if level else None
    docs = await get_documents("department", filter_dict, limit)
    return docs

# Admissions
@app.post("/admissions", response_model=dict)
async def submit_admission(apply: Admission):
    _id = await create_document("admission", apply.model_dump(by_alias=True, exclude_none=True))
    return {"id": _id, "status": "submitted"}

@app.get("/admissions")
async def list_admissions(level: Optional[str] = None, status: Optional[str] = None, limit: int = 100):
    filter_dict = {}
    if level:
        filter_dict["level"] = level
    if status:
        filter_dict["status"] = status
    docs = await get_documents("admission", filter_dict or None, limit)
    return docs

# Gallery
@app.post("/gallery", response_model=dict)
async def add_gallery_image(img: GalleryImage):
    _id = await create_document("galleryimage", img.model_dump(by_alias=True, exclude_none=True))
    return {"id": _id}

@app.get("/gallery")
async def list_gallery(level: Optional[str] = None, album: Optional[str] = None, limit: int = 100):
    filter_dict = {}
    if level:
        filter_dict["level"] = level
    if album:
        filter_dict["album"] = album
    docs = await get_documents("galleryimage", filter_dict or None, limit)
    return docs

@app.get("/test")
async def test():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}
