"""
Showbuddy Database Simulation

This module simulates a database for Showbuddy.ai, storing business card data,
transcripts, and participant information associated with session IDs.
Designed to be easily transitioned to MongoDB in the future.
"""

import json
import logging
import os
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

logger = logging.getLogger(__name__)

class Collection:
    """Base collection class that emulates MongoDB collection behavior."""

    def __init__(self, db, collection_name: str):
        """Initialize a collection with reference to database.

        Args:
            db: Reference to the main database
            collection_name: Name of the collection
        """
        self.db = db
        self.collection_name = collection_name
        self.collection_dir = os.path.join(db.storage_dir, collection_name)
        
        # Create collection directory if it doesn't exist
        if not os.path.exists(self.collection_dir):
            os.makedirs(self.collection_dir)

    def insert_one(self, document: Dict[str, Any]) -> str:
        """Insert a document into the collection.

        Args:
            document: Document to insert

        Returns:
            ID of the inserted document
        """
        # Create a new _id if one doesn't exist
        if "_id" not in document:
            document["_id"] = str(uuid.uuid4())
            
        # Add created_at and updated_at timestamps
        now = datetime.now().isoformat()
        if "created_at" not in document:
            document["created_at"] = now
        document["updated_at"] = now
        
        # Save document to file
        doc_id = document["_id"]
        file_path = os.path.join(self.collection_dir, f"{doc_id}.json")
        with open(file_path, 'w') as f:
            json.dump(document, f, indent=2)
            
        return doc_id
    
    def insert_many(self, documents: List[Dict[str, Any]]) -> List[str]:
        """Insert multiple documents into the collection.

        Args:
            documents: List of documents to insert

        Returns:
            List of IDs of the inserted documents
        """
        return [self.insert_one(doc) for doc in documents]
    
    def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a document that matches the query.

        Args:
            query: Query criteria

        Returns:
            Matching document or None if not found
        """
        # Special case for _id query
        if "_id" in query and len(query) == 1:
            doc_id = query["_id"]
            file_path = os.path.join(self.collection_dir, f"{doc_id}.json")
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return json.load(f)
            return None
            
        # Otherwise, scan all documents (inefficient but simulates the behavior)
        for filename in os.listdir(self.collection_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(self.collection_dir, filename)
                with open(file_path, 'r') as f:
                    doc = json.load(f)
                    
                # Check if document matches query
                matches = True
                for key, value in query.items():
                    if key not in doc or doc[key] != value:
                        matches = False
                        break
                
                if matches:
                    return doc
                    
        return None
    
    def find(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find all documents that match the query.

        Args:
            query: Query criteria

        Returns:
            List of matching documents
        """
        results = []
        
        # Scan all documents
        for filename in os.listdir(self.collection_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(self.collection_dir, filename)
                with open(file_path, 'r') as f:
                    doc = json.load(f)
                    
                # Check if document matches query
                matches = True
                for key, value in query.items():
                    if key not in doc or doc[key] != value:
                        matches = False
                        break
                
                if matches:
                    results.append(doc)
                    
        return results
    
    def update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        """Update a document that matches the query.

        Args:
            query: Query criteria
            update: Update operations

        Returns:
            True if a document was updated, False otherwise
        """
        # Find the document to update
        doc = self.find_one(query)
        if not doc:
            return False
            
        # Apply the update
        if "$set" in update:
            for key, value in update["$set"].items():
                doc[key] = value
        else:
            # Assume direct field updates
            for key, value in update.items():
                if key != "$set":
                    doc[key] = value
                    
        # Update the updated_at timestamp
        doc["updated_at"] = datetime.now().isoformat()
        
        # Save the updated document
        doc_id = doc["_id"]
        file_path = os.path.join(self.collection_dir, f"{doc_id}.json")
        with open(file_path, 'w') as f:
            json.dump(doc, f, indent=2)
            
        return True

class ShowbuddyDB:
    """Main database class for Showbuddy application."""

    def __init__(self, storage_dir: str = "showbuddy-data"):
        """Initialize the database with a storage directory.

        Args:
            storage_dir: Directory where database files will be stored
        """
        self.storage_dir = storage_dir
        
        # Create MongoDB-like collections
        self.cards = Collection(self, "cards")
        self.transcripts = Collection(self, "transcripts")
        self.reports = Collection(self, "reports")
        
        # Create managers that provide the required API
        self.card = CardManager(self)
        self.transcript = TranscriptManager(self)
        self.report = ReportManager(self)
        
        # Create storage directory if it doesn't exist
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)
        
        logger.info("ShowbuddyDB initialized with storage directory: %s", storage_dir)




class CardManager:
    """Manager for business card data."""

    def __init__(self, db: ShowbuddyDB):
        """Initialize with reference to main database.

        Args:
            db: Reference to the main ShowbuddyDB instance
        """
        self.db = db

    def add(self, session_id: str, card_data: Dict[str, Any]) -> None:
        """Add a business card to the database.

        Args:
            session_id: Unique ID for the recording session
            card_data: Dictionary containing business card information
        """
        # Add session_id and timestamp to card data
        card_data["session_id"] = session_id
        card_data["timestamp"] = datetime.now().isoformat()
        
        # Insert the card into the cards collection
        self.db.cards.insert_one(card_data)

    def get_all_cards(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all business cards for a session.

        Args:
            session_id: Unique ID for the recording session

        Returns:
            List of dictionaries containing business card data
        """
        # Find all cards with matching session_id
        return self.db.cards.find({"session_id": session_id})


class TranscriptManager:
    """Manager for transcript data."""

    def __init__(self, db: ShowbuddyDB):
        """Initialize with reference to main database.

        Args:
            db: Reference to the main ShowbuddyDB instance
        """
        self.db = db

    def add(self, session_id: str, transcript: Dict[str, Any]) -> None:
        """Add a transcript to the database.

        Args:
            session_id: Unique ID for the recording session
            transcript: Dictionary containing transcript information
        """
        # Add session_id to transcript data
        transcript["session_id"] = session_id
        
        # Check if transcript for this session already exists
        existing = self.db.transcripts.find_one({"session_id": session_id})
        
        if existing:
            # Update existing transcript
            self.db.transcripts.update_one(
                {"_id": existing["_id"]},
                {"$set": transcript}
            )
        else:
            # Insert new transcript
            self.db.transcripts.insert_one(transcript)

    def get(self, session_id: str) -> Dict[str, Any]:
        """Get the transcript for a session.

        Args:
            session_id: Unique ID for the recording session

        Returns:
            Dictionary containing transcript data
        """
        transcript = self.db.transcripts.find_one({"session_id": session_id})
        return transcript or {}

    def get_text(self, session_id: str) -> str:
        """Get the transcript text for a session.

        Args:
            session_id: Unique ID for the recording session

        Returns:
            Transcript as a block of text
        """
        transcript = self.get(session_id)
        
        # If the transcript exists and has a 'text' field, return it
        if transcript and "text" in transcript:
            return transcript["text"]
        
        # If the transcript exists and has a 'segments' field, combine all segments
        if transcript and "segments" in transcript:
            segments = transcript["segments"]
            text_parts = []
            
            for segment in segments:
                if "speaker" in segment and "text" in segment:
                    speaker = segment["speaker"]
                    text = segment["text"]
                    text_parts.append(f"{speaker}: {text}")
                elif "text" in segment:
                    text_parts.append(segment["text"])
            
            return "\n".join(text_parts)
        
        return ""


class ReportManager:
    """Manager for report data."""


    def __init__(self, db: ShowbuddyDB):
        """Initialize with reference to main database.

        Args:
            db: Reference to the main ShowbuddyDB instance
        """
        self.db = db

    def add(self, session_id: str, report_data: Dict[str, Any]) -> None:
        """Add a participant to the database.

        Args:
            session_id: Unique ID for the recording session
            report_data: Dictionary containing report information
        """

        # Add session_id to participant data
        report_data["session_id"] = session_id
        
        # Check if participant already exists
        existing = self.db.participants.find_one({
            "session_id": session_id,
            "participant_id": participant_id
        })
        
        if existing:
            # Update existing participant
            self.db.participants.update_one(
                {"_id": existing["_id"]},
                {"$set": participant_data}
            )
        else:
            # Insert new participant
            self.db.participants.insert_one(participant_data)

# Create a global instance for easy imports
db = ShowbuddyDB()


class MongoDBAdapter:
    """
    Adapter class to migrate from the file-based DB to MongoDB.
    This is a skeleton implementation to show the transition path.
    """
    
    def __init__(self, connection_string=None, db_name="showbuddy"):
        """
        Initialize MongoDB connection.
        
        Args:
            connection_string: MongoDB connection string
            db_name: Name of the database
        """
        self.connected = False
        try:
            # Attempt to import pymongo - this will fail in the current implementation
            # but would be needed when transitioning to real MongoDB
            import pymongo
            self.client = pymongo.MongoClient(connection_string)
            self.db = self.client[db_name]
            self.connected = True
            
            # Create collections
            self.cards = self.db["cards"]
            self.transcripts = self.db["transcripts"]
            self.reports = self.db["reports"]

            
            # Create indexes
            self.cards.create_index([("session_id", 1)])
            self.transcripts.create_index([("session_id", 1)], unique=True)
            self.reports.create_index([("session_id", 1), ("report_id", 1)], unique=True)
            
        except ImportError:
            print("PyMongo not available. Using file-based database simulation.")
    
    def migrate_from_file_based(self, file_db: ShowbuddyDB):
        """
        Migrate data from file-based database to MongoDB.
        
        Args:
            file_db: File-based database instance
        """
        if not self.connected:
            print("MongoDB not connected. Cannot migrate.")
            return
            
        # Implementation would iterate through all files in each collection
        # directory and insert them into MongoDB collections
        pass


# Example usage:
if __name__ == "__main__":
    # Example session ID
    session_id = "session_123"
    
    # Add business cards
    db.card.add(session_id, {
        "name": "John Doe",
        "company": "Acme Inc",
        "position": "CEO",
        "email": "john@acme.com",
        "phone": "123-456-7890"
    })
    
    # Add transcript
    db.transcript.add(session_id, {
        "session_start": "2025-04-03T10:30:00",
        "session_end": "2025-04-03T11:15:00",
        "segments": [
            {"speaker": "Speaker_1", "text": "Hello, welcome to our booth!", "timestamp": "2025-04-03T10:30:15"},
            {"speaker": "Speaker_2", "text": "Thanks! I'm interested in your products.", "timestamp": "2025-04-03T10:30:20"}
        ]
    })
    
    # Add participants
    db.participant.add(session_id, {
        "participant_id": "Speaker_1",
        "name": "Jane Smith",
        "role": "Sales Representative",
        "company": "Monatea"
    })
    
    db.participant.add(session_id, {
        "participant_id": "Speaker_2",
        "name": "John Doe",
        "role": "CEO",
        "company": "Acme Inc"
    })
    
    # Update feedback
    db.participant.update_feedback(session_id, "Speaker_2", {
        "sentiment": "positive",
        "follow_up_actions": ["Send product catalog", "Schedule demo"]
    })
    
    # Get all cards
    print("All Cards:", db.card.get_all_cards(session_id))
    
    # Get transcript
    print("Transcript Text:", db.transcript.get_text(session_id))
    
    # Get participant feedback
    print("Participant Feedback:", db.participant.get_feedback(session_id, "Speaker_2"))
    
    # Get all participant IDs
    print("Participant IDs:", db.participant.get_ids(session_id))
    
    # Example of MongoDB migration (would be executed when ready to migrate)
    # mongo_db = MongoDBAdapter("mongodb://localhost:27017/")
    # mongo_db.migrate_from_file_based(db)