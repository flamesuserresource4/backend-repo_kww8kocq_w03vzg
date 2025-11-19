from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# Each model corresponds to a MongoDB collection using class name lowercased

class BaseDocument(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Notice(BaseDocument):
    title: str
    content: str
    audience: str = Field(pattern="^(school|college|both)$")
    category: str = Field(default="general")
    date: datetime = Field(default_factory=datetime.utcnow)

class Event(BaseDocument):
    title: str
    description: str
    start_date: datetime
    end_date: Optional[datetime] = None
    audience: str = Field(pattern="^(school|college|both)$")
    location: Optional[str] = None

class Faculty(BaseDocument):
    name: str
    designation: str
    department: str
    level: str = Field(pattern="^(school|college)$")
    bio: Optional[str] = None
    photo_url: Optional[str] = None

class Department(BaseDocument):
    name: str
    description: Optional[str] = None
    head: Optional[str] = None
    level: str = Field(pattern="^(school|college|both)$")
    subjects: List[str] = []

class Admission(BaseDocument):
    level: str = Field(pattern="^(school|college)$")
    first_name: str
    last_name: str
    class_or_stream: str  # Class (6-10) for school or Stream (Science/Arts/Commerce) for college
    phone: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    guardian_name: Optional[str] = None
    previous_institution: Optional[str] = None
    status: str = Field(default="submitted", pattern="^(submitted|reviewed|accepted|rejected)$")

class GalleryImage(BaseDocument):
    title: str
    url: str
    description: Optional[str] = None
    level: str = Field(pattern="^(school|college|both)$")
    album: Optional[str] = None
