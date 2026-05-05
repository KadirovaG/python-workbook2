# storage.py
import json
import os
from datetime import datetime


class JsonStorage:
    """Saves and retrieves messages from a local JSON file."""

    def __init__(self, filepath: str = "messages.json") -> None:
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self) -> None:
        """Create an empty JSON array if the file does not exist."""
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump([], f)

    def save(self, chat_id: int, username: str, text: str) -> None:
        """Append one message record to the file."""
        records = self.load_all()
        records.append(
            {
                "chat_id": chat_id,
                "username": username,
                "text": text,
                "received_at": datetime.now().isoformat(),
            }
        )
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)

    def load_all(self) -> list:
        """Return all records as a list of dicts."""
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def count(self) -> int:
        """Return the total number of saved messages."""
        return len(self.load_all())
