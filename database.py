import sqlite3
import os
import sys
from time import time

def connect_db():
    # Get AppData directory
    appdata = os.environ.get("APPDATA")

    app_dir = os.path.join(appdata, "Rem")

    # Ensure directory exists
    os.makedirs(app_dir, exist_ok=True)

    # Database path
    db_path = os.path.join(app_dir, "rem.db")

    return sqlite3.connect(db_path)

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            date TEXT,
            time TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_reminder(title, date, time):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reminders (title, date, time) VALUES (?, ?, ?)",
        (title, date, time)
    )
    conn.commit()
    conn.close()

def get_all_reminders():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, date, time FROM reminders ORDER BY date, time")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_reminder(reminder_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reminders WHERE id=?", (reminder_id,))
    conn.commit()
    conn.close()