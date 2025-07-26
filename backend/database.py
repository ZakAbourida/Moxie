from motor.motor_asyncio import AsyncIOMotorClient
import os
from typing import Optional, List, Dict, Any
from datetime import datetime

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'athletica')]

class DatabaseManager:
    def __init__(self):
        self.db = db
    
    async def create_document(self, collection: str, document: dict) -> dict:
        """Create a new document in the specified collection."""
        document['created_at'] = datetime.utcnow()
        document['updated_at'] = datetime.utcnow()
        result = await self.db[collection].insert_one(document)
        document['_id'] = str(result.inserted_id)
        return document
    
    async def get_document(self, collection: str, doc_id: str) -> Optional[dict]:
        """Get a document by ID."""
        document = await self.db[collection].find_one({"id": doc_id})
        if document:
            document.pop('_id', None)  # Remove MongoDB ObjectId
        return document
    
    async def get_documents(self, collection: str, filter_query: dict = None, limit: int = 1000) -> List[dict]:
        """Get documents with optional filtering."""
        if filter_query is None:
            filter_query = {}
        
        cursor = self.db[collection].find(filter_query).limit(limit)
        documents = await cursor.to_list(length=limit)
        
        # Remove MongoDB ObjectIds
        for doc in documents:
            doc.pop('_id', None)
        
        return documents
    
    async def update_document(self, collection: str, doc_id: str, update_data: dict) -> Optional[dict]:
        """Update a document by ID."""
        update_data['updated_at'] = datetime.utcnow()
        
        result = await self.db[collection].update_one(
            {"id": doc_id},
            {"$set": update_data}
        )
        
        if result.matched_count > 0:
            return await self.get_document(collection, doc_id)
        return None
    
    async def delete_document(self, collection: str, doc_id: str) -> bool:
        """Delete a document by ID."""
        result = await self.db[collection].delete_one({"id": doc_id})
        return result.deleted_count > 0
    
    async def find_documents(self, collection: str, query: dict, limit: int = 1000) -> List[dict]:
        """Find documents matching a query."""
        cursor = self.db[collection].find(query).limit(limit)
        documents = await cursor.to_list(length=limit)
        
        # Remove MongoDB ObjectIds
        for doc in documents:
            doc.pop('_id', None)
        
        return documents
    
    async def find_one(self, collection: str, query: dict) -> Optional[dict]:
        """Find one document matching a query."""
        document = await self.db[collection].find_one(query)
        if document:
            document.pop('_id', None)
        return document
    
    async def count_documents(self, collection: str, query: dict = None) -> int:
        """Count documents matching a query."""
        if query is None:
            query = {}
        return await self.db[collection].count_documents(query)
    
    async def aggregate(self, collection: str, pipeline: List[dict]) -> List[dict]:
        """Run an aggregation pipeline."""
        cursor = self.db[collection].aggregate(pipeline)
        documents = await cursor.to_list(length=1000)
        
        # Remove MongoDB ObjectIds
        for doc in documents:
            doc.pop('_id', None)
        
        return documents

# Global database manager instance
db_manager = DatabaseManager()

# Collection names
COLLECTIONS = {
    'users': 'users',
    'athletes': 'athletes',
    'goals': 'goals',
    'programs': 'programs',
    'sessions': 'sessions',
    'exercises': 'exercises',
    'session_exercises': 'session_exercises',
    'personal_records': 'personal_records',
    'physical_assessments': 'physical_assessments',
    'events': 'events',
    'event_entries': 'event_entries',
    'session_templates': 'session_templates'
}