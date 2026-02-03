import time
import sqlite3
from datetime import datetime
from tkinter import messagebox

def check_reminders():
    while True:
        time.sleep(60)  # Check every minute

        conn = sqlite3.connect("reminders.db")
        cursor = conn.cursor()
        now_date = datetime.now().strftime("%Y-%m-%d")
        now_time = datetime.now().strftime("%H:%M")

        cursor.execute("SELECT id, title, date, time FROM reminders WHERE date=? AND time=?", (now_date, now_time))
        for rem in cursor.fetchall():
            messagebox.showinfo("Reminder", rem[0])
        
        conn.close()
        time.sleep(60)

        