import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any

class PostStorage:
    def __init__(self, db_path="~/.local/share/shitposter/posts.db"):
        self.db_path = os.path.expanduser(db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def init_db(self):
        """Initialize SQLite database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS scheduled_posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    platform TEXT NOT NULL,
                    content TEXT NOT NULL,
                    schedule_time DATETIME NOT NULL,
                    status TEXT DEFAULT 'pending',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def add_post(self, platform: str, content: str, schedule_time: datetime) -> int:
        """Add a scheduled post"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO scheduled_posts (platform, content, schedule_time) VALUES (?, ?, ?)",
                (platform, content, schedule_time.isoformat())
            )
            return cursor.lastrowid

    def get_pending_posts(self) -> List[Dict[str, Any]]:
        """Get all pending posts"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM scheduled_posts WHERE status = 'pending' AND schedule_time <= datetime('now')"
            )
            return [dict(row) for row in cursor.fetchall()]

    def mark_post_completed(self, post_id: int):
        """Mark a post as completed"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE scheduled_posts SET status = 'completed' WHERE id = ?",
                (post_id,)
            )

    def mark_post_failed(self, post_id: int, error: str):
        """Mark a post as failed"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE scheduled_posts SET status = 'failed', error = ? WHERE id = ?",
                (error, post_id)
            )