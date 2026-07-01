import datetime
from database import get_connection


class ReminderManager:
    def __init__(self, ui_refresh_callback=0):
        self.refresh_ui = ui_refresh_callback

    def add_reminder(self, command_text):
        content = command_text.replace("add schedule", "").replace("schedule", "").replace("remind me to", "").replace(
            "reminder", "").strip()
        if not content:
            return "What event are we scheduling, Boss?"

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        with get_connection() as conn:
            conn.execute("INSERT INTO schedule (event, time) VALUES (?, ?)", (content, timestamp))
            conn.commit()

        if self.refresh_ui:
            self.refresh_ui()  # Triggers Real-time UI Pipeline update
        return f"Understood, Boss. Scheduled: {content}."

    def fetch_active_reminders(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT event, time FROM schedule ORDER BY id DESC LIMIT 5")
            return [f"{row[0]} ({row[1]})" for row in cursor.fetchall()]