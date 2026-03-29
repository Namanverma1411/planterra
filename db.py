import os
import uuid

class MockCollection:
    def __init__(self, name):
        self.name = name
        self.data = []

    def insert_one(self, doc):
        doc['_id'] = str(uuid.uuid4())
        self.data.append(doc)
        class Result:
             inserted_id = doc['_id']
        return Result()

    def find_one(self, query):
        for doc in self.data:
            match = True
            for k, v in query.items():
                if str(v) != str(doc.get(k)):  # Stringify for easy ObjectId bypass
                    match = False
                    break
            if match:
                return dict(doc)
        return None

    def find(self, query):
        results = []
        for doc in self.data:
            match = True
            for k, v in query.items():
                if str(v) != str(doc.get(k)):
                    match = False
                    break
            if match:
                results.append(dict(doc))
        return results

    def update_one(self, query, update):
        for doc in self.data:
            match = True
            for k, v in query.items():
                if str(v) != str(doc.get(k)):
                    match = False
                    break
            if match:
                if "$set" in update:
                    doc.update(update["$set"])
                return

    def delete_one(self, query):
        for i, doc in enumerate(self.data):
            match = True
            for k, v in query.items():
                if str(v) != str(doc.get(k)):
                    match = False
                    break
            if match:
                del self.data[i]
                return

class MockDB:
    def __init__(self):
        self.users = MockCollection("users")
        self.tasks = MockCollection("tasks")
    
    def __getitem__(self, name):
        if name == "users": return self.users
        return self.tasks

# Keep a global instance so data stays in memory while the server runs
_mock_db = MockDB()

def get_db():
    print("✅ Using Mock In-Memory Database! (No MongoDB required)")
    return _mock_db
