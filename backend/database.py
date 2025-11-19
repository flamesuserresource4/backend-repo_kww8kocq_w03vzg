from typing import Any, Dict, Optional, List
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import os
from datetime import datetime

DB_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DATABASE_NAME", "school_college_db")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None

async def get_db() -> AsyncIOMotorDatabase:
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(DB_URL)
        _db = _client[DB_NAME]
    return _db

async def create_document(collection_name: str, data: Dict[str, Any]) -> str:
    db = await get_db()
    now = datetime.utcnow()
    data["created_at"] = now
    data["updated_at"] = now
    result = await db[collection_name].insert_one(data)
    return str(result.inserted_id)

async def get_documents(collection_name: str, filter_dict: Dict[str, Any] | None = None, limit: int = 50) -> List[Dict[str, Any]]:
    db = await get_db()
    cursor = db[collection_name].find(filter_dict or {}).limit(limit)
    docs = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        docs.append(doc)
    return docs

async def update_document(collection_name: str, doc_id, data: Dict[str, Any]) -> int:
    from bson import ObjectId
    db = await get_db()
    data["updated_at"] = datetime.utcnow()
    result = await db[collection_name].update_one({"_id": ObjectId(doc_id)}, {"$set": data})
    return result.modified_count

async def delete_document(collection_name: str, doc_id) -> int:
    from bson import ObjectId
    db = await get_db()
    result = await db[collection_name].delete_one({"_id": ObjectId(doc_id)})
    return result.deleted_count
