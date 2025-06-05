import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('chat_history.db')
        self.create_tables()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            assistant_message TEXT NOT NULL,
            model_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'todo',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        self.conn.commit()
        
    async def save_conversation(self, user_message: str, assistant_message: str, model_name: str):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO conversations (user_message, assistant_message, model_name)
        VALUES (?, ?, ?)
        ''', (user_message, assistant_message, model_name))
        self.conn.commit()
        
    async def get_conversations(self, limit: int = 100):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT * FROM conversations
        ORDER BY created_at DESC
        LIMIT ?
        ''', (limit,))
        return cursor.fetchall()

    async def create_task(self, title: str, description: str = '', status: str = 'todo'):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO tasks (title, description, status)
        VALUES (?, ?, ?)
        ''', (title, description, status))
        self.conn.commit()
        return cursor.lastrowid

    async def get_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT id, title, description, status, created_at
        FROM tasks
        ORDER BY created_at DESC
        ''')
        return cursor.fetchall()

    async def get_task(self, task_id: int):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT id, title, description, status, created_at
        FROM tasks WHERE id = ?
        ''', (task_id,))
        return cursor.fetchone()

    async def update_task_status(self, task_id: int, status: str):
        cursor = self.conn.cursor()
        cursor.execute('''
        UPDATE tasks SET status = ? WHERE id = ?
        ''', (status, task_id))
        self.conn.commit()
        return await self.get_task(task_id)
