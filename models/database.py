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