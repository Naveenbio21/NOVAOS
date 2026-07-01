import datetime
from database import get_connection


class TaskManager:
    def __init__(self, ui_refresh_callback=0):
        self.refresh_ui = ui_refresh_callback

    def add_task(self, command_text):
        content = command_text.replace("add task", "").replace("task", "").replace("todo", "").replace("to do",
                                                                                                       "").strip()
        if not content:
            return "What task are we tracking, Boss?"

        with get_connection() as conn:
            conn.execute("INSERT INTO tasks (task, status) VALUES (?, 'Pending')", (content,))
            conn.commit()

        if self.refresh_ui:
            self.refresh_ui()  # Triggers Real-time UI Pipeline update
        return f"Task added to the queue, Boss: {content}."

    def fetch_pending_tasks(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT task FROM tasks WHERE status='Pending' ORDER BY id DESC LIMIT 5")
            return [row[0] for row in cursor.fetchall()]