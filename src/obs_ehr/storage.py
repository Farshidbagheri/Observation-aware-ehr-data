"""Two matched document/query implementations. No perf claim without real measurement."""
from __future__ import annotations
import json
import os
import sqlite3
from pathlib import Path
from .core import asof_reference

class SQLiteStore:
    def __init__(self, path: str | Path = ":memory:"):
        self.conn = sqlite3.connect(str(path))
        self.conn.execute('''CREATE TABLE IF NOT EXISTS events (
            event_id TEXT PRIMARY KEY, stay_id TEXT NOT NULL,
            available_at TEXT, payload_json TEXT NOT NULL)''')
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_stay_avail ON events(stay_id,available_at)')

    def replace(self, records: list[dict]) -> None:
        with self.conn:
            self.conn.execute("DELETE FROM events")
            self.conn.executemany(
                "INSERT INTO events(event_id,stay_id,available_at,payload_json) VALUES(?,?,?,?)",
                [(e["event_id"],e["stay_id"],e.get("available_at"),json.dumps(e,sort_keys=True)) for e in records])

    def asof(self, stay_id: str, landmark: str) -> list[dict]:
        cursor = self.conn.execute('''SELECT payload_json FROM events
            WHERE stay_id=? AND available_at IS NOT NULL AND available_at<=?
            ORDER BY available_at,event_id''',(str(stay_id),landmark))
        return [json.loads(x[0]) for x in cursor.fetchall()]

    def close(self):
        self.conn.close()


class MongoStore:
    def __init__(self, uri: str | None = None, db: str="obs_ehr_benchmark"):
        try:
            from pymongo import MongoClient, ASCENDING
        except ImportError as e:
            raise RuntimeError("MongoDB runs need pip install -e '.[mongo]'") from e
        self.client=MongoClient(uri or os.getenv("MONGODB_URI","mongodb://localhost:27017"),serverSelectionTimeoutMS=4000)
        self.client.admin.command("ping")
        self.collection=self.client[db]["events"]
        self.collection.create_index([("event_id",ASCENDING)],unique=True)
        self.collection.create_index([("stay_id",ASCENDING),("available_at",ASCENDING)])

    def replace(self,records: list[dict]):
        self.collection.delete_many({})
        if records:
            self.collection.insert_many([{**r,"_id":r["event_id"]} for r in records],ordered=False)

    def asof(self,stay_id: str,landmark: str) -> list[dict]:
        cursor=self.collection.find({"stay_id":str(stay_id),"available_at":{"$ne":None,"$lte":landmark}}, {"_id":0}).sort([("available_at",1),("event_id",1)])
        return list(cursor)

    def close(self):
        self.client.close()
