import os
import threading
import time
import tkinter as tk
from tkinter import filedialog
import speech_recognition as sr

# Core image processing for crisp high-resolution rendering
from PIL import Image, ImageTk

# Import back-end integrator module safely
import nova_os

# PREMIUM NEON MATRIX DESIGN THEME
COLOR_DARK_HEX = "#011627"
COLOR_DEEP_HEX = "#00618a"
COLOR_BRIGHT = "#00f2fe"  # Neon Aqua Cyan
COLOR_SEA = "#4facfe"  # Deep Tech Blue
COLOR_CARD_BG = "#0c273a"  # Glassmorphic Card Background
COLOR_CARD_BORDER = "#144361"  # Semi-transparent structural rim
COLOR_TEXT_MAIN = "#ffffff"  # High-contrast white
COLOR_TEXT_MUTED = "#8cbcd0"  # System light gray-blue
COLOR_TEXT_DARK = "#011627"  # High-density dark gray


class NovaOSApp:
    def __init__(self, main_root):
        self.root = main_root
        self.root.title("Nova OS Cognitive Engine")
        self.root.geometry("420x680")
        self.root.configure(bg=COLOR_DARK_HEX)
        self.root.resizable(False, False)

        # Persistent storage configuration to secure images against garbage collection
        self.avatar_img = None

        # ----------------------------------------------------
        # 1. GRADIENT BACKDROP MATRIX (Draw Layer)
        # ----------------------------------------------------
        self.bg_canvas = tk.Canvas(main_root, width=420, height=680,
                                   bg=COLOR_DARK_HEX, bd=0, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1.0, relheight=1.0)
        self.draw_gradient_matrix()

        # ----------------------------------------------------
        # 2. INNER WORKSPACE CONTAINER
        # ----------------------------------------------------
        self.app_screen = tk.Frame(main_root, bg="", bd=0)
        self.app_screen.place(x=0, y=0, relwidth=1.0, relheight=1.0)

        # Device Top Status Bar Space (Indian Time Zone Tracker Entry)
        self.status_bar = tk.Frame(self.app_screen, bg=COLOR_DARK_HEX, height=20)
        self.status_bar.pack(fill=tk.X, side=tk.TOP)
        self.status_bar_lbl = tk.Label(self.status_bar, text="System Synchronized", font=("Segoe UI", 8, "bold"),
                                       fg=COLOR_BRIGHT, bg=COLOR_DARK_HEX)
        self.status_bar_lbl.pack(side=tk.RIGHT, padx=20)

        # Header Profile Block Layout
        self.header_frame = tk.Frame(self.app_screen, bg=COLOR_DARK_HEX, padx=24, pady=6)
        self.header_frame.pack(fill=tk.X)

        # --- Dynamic Profile Avatar Core ---
        self.avatar_canvas = tk.Canvas(self.header_frame, width=44, height=44,
                                       bg=COLOR_DARK_HEX, bd=0, highlightthickness=0)
        self.avatar_canvas.pack(side=tk.LEFT, padx=(0, 12))

        # Load and fit avatar image asset
        self.load_avatar_asset()

        self.greeting_frame = tk.Frame(self.header_frame, bg=COLOR_DARK_HEX)
        self.greeting_frame.pack(side=tk.LEFT)
        tk.Label(self.greeting_frame, text="Nova, OS", font=("Segoe UI", 11, "bold"),
                 fg=COLOR_TEXT_MAIN, bg=COLOR_DARK_HEX).pack(anchor=tk.W)
        self.greeting_frame_sub = tk.Label(self.greeting_frame, text="Awaiting Responses...",
                                           font=("Segoe UI", 8),
                                           fg=COLOR_BRIGHT, bg=COLOR_DARK_HEX)
        self.greeting_frame_sub.pack(anchor=tk.W)

        # ----------------------------------------------------
        # 3. INTERACTIVE ASSISTANT HUB (Pulse Visualizer)
        # ----------------------------------------------------
        self.hub_frame = tk.Frame(self.app_screen, bg=COLOR_DARK_HEX, pady=8)
        self.hub_frame.pack(fill=tk.X)

        self.mic_canvas = tk.Canvas(self.hub_frame, width=76, height=76,
                                    bg=COLOR_DARK_HEX, bd=0, highlightthickness=0)
        self.mic_canvas.pack(pady=2)
        self.mic_canvas.create_oval(10, 10, 66, 66, fill=COLOR_BRIGHT, outline=COLOR_SEA, width=3)
        self.mic_canvas.create_text(38, 38, text="🎙", font=("Segoe UI", 18), fill=COLOR_TEXT_DARK)

        self.status_lbl = tk.Label(self.hub_frame, text="Core Activated!",
                                   font=("Segoe UI", 9, "italic"), fg=COLOR_BRIGHT, bg=COLOR_DARK_HEX)
        self.status_lbl.pack()

        # ----------------------------------------------------
        # 4. COLUMNS DASHBOARD GRID (Real-time Efficient Stream Views)
        # ----------------------------------------------------
        self.grid_frame = tk.Frame(self.app_screen, bg=COLOR_DARK_HEX, padx=20, pady=5)
        self.grid_frame.pack(fill=tk.BOTH, expand=True)

        # --- High Efficiency Task Column Card ---
        self.task_card = tk.Frame(self.grid_frame, bg=COLOR_CARD_BG, bd=1, highlightbackground=COLOR_CARD_BORDER,
                                  highlightthickness=1)
        self.task_card.pack(fill=tk.X, pady=(0, 6), ipady=4)

        self.task_header = tk.Frame(self.task_card, bg=COLOR_CARD_BG, padx=12, pady=4)
        self.task_header.pack(fill=tk.X)
        tk.Label(self.task_header, text="Task Stream", font=("Segoe UI", 9, "bold"), fg=COLOR_TEXT_MAIN,
                 bg=COLOR_CARD_BG).pack(side=tk.LEFT)

        self.task_list_container = tk.Frame(self.task_card, bg=COLOR_CARD_BG, padx=12)
        self.task_list_container.pack(fill=tk.X)

        # --- Dynamic Indian Standard Time Reminders Card ---
        self.rem_card = tk.Frame(self.grid_frame, bg=COLOR_CARD_BG, bd=1, highlightbackground=COLOR_CARD_BORDER,
                                 highlightthickness=1)
        self.rem_card.pack(fill=tk.X, pady=4, ipady=4)

        self.rem_header = tk.Frame(self.rem_card, bg=COLOR_CARD_BG, padx=12, pady=4)
        self.rem_header.pack(fill=tk.X)
        tk.Label(self.rem_header, text="High-Priority Scheduler (IST)", font=("Segoe UI", 9, "bold"),
                 fg=COLOR_TEXT_MAIN,
                 bg=COLOR_CARD_BG).pack(side=tk.LEFT)

        self.rem_list_container = tk.Frame(self.rem_card, bg=COLOR_CARD_BG, padx=12)
        self.rem_list_container.pack(fill=tk.X)

        # ----------------------------------------------------
        # 5. CONSOLE LOG MATRIX WINDOW
        # ----------------------------------------------------
        self.chat_box = tk.Text(self.grid_frame, height=4, wrap=tk.WORD, state=tk.DISABLED,
                                bg=COLOR_DARK_HEX, fg=COLOR_TEXT_MAIN, font=("Segoe UI", 9),
                                bd=0, highlightthickness=1, highlightbackground=COLOR_CARD_BORDER)
        self.chat_box.pack(fill=tk.BOTH, expand=True, pady=6)

        # ----------------------------------------------------
        # 6. MOBILE APP CONTROL BAR (Input Field Row)
        # ----------------------------------------------------
        self.control_bar = tk.Frame(self.app_screen, bg=COLOR_DARK_HEX, padx=15, pady=8)
        self.control_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.file_btn = tk.Button(self.control_bar, text="📎", font=("Segoe UI", 11), bg=COLOR_CARD_BG,
                                  fg=COLOR_TEXT_MAIN, activebackground=COLOR_SEA, activeforeground=COLOR_TEXT_DARK,
                                  bd=0, padx=8, cursor="hand2", command=self.handle_file_upload)
        self.file_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.text_entry = tk.Entry(self.control_bar, bg="#FFFFFF", fg=COLOR_TEXT_DARK, font=("Segoe UI", 10),
                                   insertbackground=COLOR_TEXT_DARK, bd=0, highlightthickness=1,
                                   highlightbackground=COLOR_CARD_BORDER, highlightcolor=COLOR_BRIGHT)
        self.text_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3, padx=(0, 5))
        self.text_entry.bind("<Return>", lambda event: self.process_text_input())

        self.send_btn = tk.Button(self.control_bar, text="Run", font=("Segoe UI", 8, "bold"), bg=COLOR_BRIGHT,
                                  fg=COLOR_TEXT_DARK, activebackground=COLOR_SEA, activeforeground=COLOR_TEXT_MAIN,
                                  bd=0, padx=12, cursor="hand2", command=self.process_text_input)
        self.send_btn.pack(side=tk.RIGHT)

        # Core Micro Listener Execution Trigger
        self.mic_canvas.bind("<Button-1>", lambda event: self.start_listening_thread())

        # Render Core Real-Time Dynamic List Matrices
        self.realtime_refresh_lists()

        # Initialize High-Priority Realtime Scheduler Core Daemon thread
        self.start_reminder_daemon()
        self.root.after(500, self.trigger_initial_greeting)

    def load_avatar_asset(self):
        """Loads, centers, cuts, and scales nova_avatar.jpg down safely using standard Pillow filters."""
        img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nova_avatar.jpg")

        if os.path.exists(img_path):
            try:
                pil_img = Image.open(img_path)
                w, h = pil_img.size
                min_dim = min(w, h)
                left = (w - min_dim) / 2
                top = (h - min_dim) / 2
                right = (w + min_dim) / 2
                bottom = (h + min_dim) / 2
                pil_img = pil_img.crop((left, top, right, bottom))

                try:
                    resample_filter = Image.Resampling.LANCZOS
                except AttributeError:
                    resample_filter = Image.ANTIALIAS

                pil_img = pil_img.resize((40, 40), resample_filter)
                self.avatar_img = ImageTk.PhotoImage(pil_img)
                self.avatar_canvas.create_image(22, 22, image=self.avatar_img)
                self.avatar_canvas.create_oval(2, 2, 42, 42, outline=COLOR_BRIGHT, width=2)
                return
            except Exception as e:
                print(f"Error loading avatar image matrix: {e}")

        self.avatar_canvas.create_oval(2, 2, 42, 42, fill=COLOR_SEA, outline=COLOR_BRIGHT, width=2)

    def draw_gradient_matrix(self):
        for y in range(680):
            factor = y / 680.0
            r = int(1 + (0 - 1) * factor)
            g = int(22 + (97 - 22) * factor)
            b = int(39 + (138 - 39) * factor)
            color_hex = f"#{r:02x}{g:02x}{b:02x}"
            self.bg_canvas.create_line(0, y, 420, y, fill=color_hex)

    def realtime_refresh_lists(self):
        """Fetches pending data structures and clears/re-draws clean list items in real-time."""
        for widget in self.task_list_container.winfo_children():
            widget.destroy()
        for widget in self.rem_list_container.winfo_children():
            widget.destroy()

        try:
            with nova_os.sqlite3.connect(nova_os.DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT task FROM tasks WHERE status='Pending' ORDER BY id DESC LIMIT 2")
                tasks_rows = cursor.fetchall()

                cursor.execute("SELECT event, time FROM schedule ORDER BY id DESC LIMIT 2")
                schedule_rows = cursor.fetchall()
        except Exception:
            tasks_rows, schedule_rows = [], []

        if not tasks_rows:
            lbl = tk.Label(self.task_list_container, text="All operational objectives clear, Boss.",
                           font=("Segoe UI", 8), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD_BG)
            lbl.pack(anchor=tk.W, pady=2)
        else:
            for row in tasks_rows:
                item_frame = tk.Frame(self.task_list_container, bg=COLOR_CARD_BG)
                item_frame.pack(fill=tk.X, pady=2)
                chk = tk.Label(item_frame, text="▢", font=("Segoe UI", 9), fg=COLOR_SEA, bg=COLOR_CARD_BG)
                chk.pack(side=tk.LEFT, padx=(0, 6))
                txt = tk.Label(item_frame, text=row[0], font=("Segoe UI", 8), fg=COLOR_TEXT_MAIN, bg=COLOR_CARD_BG,
                               anchor=tk.W)
                txt.pack(side=tk.LEFT, fill=tk.X)

        if not schedule_rows:
            lbl = tk.Label(self.rem_list_container, text="No system intervals queued.",
                           font=("Segoe UI", 8), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD_BG)
            lbl.pack(anchor=tk.W, pady=2)
        else:
            for row in schedule_rows:
                item_frame = tk.Frame(self.rem_list_container, bg=COLOR_CARD_BG)
                item_frame.pack(fill=tk.X, pady=2)
                txt_title = tk.Label(item_frame, text=f"• {row[0]}", font=("Segoe UI", 8, "bold"), fg=COLOR_TEXT_MAIN,
                                     bg=COLOR_CARD_BG, anchor=tk.W)
                txt_title.pack(anchor=tk.W)
                txt_time = tk.Label(item_frame, text=f"  🕒 {row[1]}", font=("Segoe UI", 8), fg=COLOR_BRIGHT,
                                    bg=COLOR_CARD_BG, anchor=tk.W)
                txt_time.pack(anchor=tk.W)

    def start_reminder_daemon(self):
        """Monitors system intervals against Indian Standard Time frames every 30 seconds."""

        def alarm_checker():
            while True:
                time.sleep(30)
                # Formats precisely matches database storage timestamps (YYYY-MM-DD HH:M) or hours check
                ist_now = nova_os.get_ist_time()
                minute_check = ist_now.strftime("%Y-%m-%d %H:%M")
                time_only_check = ist_now.strftime("%H:%M")

                try:
                    with nova_os.sqlite3.connect(nova_os.DB_PATH) as conn:
                        c = conn.cursor()
                        # Checks for full string matches or time matches inside the matrix
                        c.execute("SELECT event FROM schedule WHERE time=? OR time LIKE ?",
                                  (minute_check, f"%{time_only_check}%"))
                        matches = c.fetchall()
                        for match in matches:
                            alert_msg = f"High Priority Notification, Boss: {match[0]} is due now!"
                            self.append_chat("ALERT", alert_msg)
                            threading.Thread(target=lambda: nova_os.speak(alert_msg), daemon=True).start()
                except Exception:
                    pass

        threading.Thread(target=alarm_checker, daemon=True).start()

    def trigger_initial_greeting(self):
        greeting = f"Nova Version 1.2.0, System online. Welcome back, Boss. All subroutines await your command."
        self.append_chat("NOVA", greeting)
        nova_os.speak(greeting)

    def append_chat(self, sender, text):
        self.root.after(0, self._safe_append_chat, sender, text)

    def _safe_append_chat(self, sender, text):
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, f"[{sender}]: {text}\n\n")
        self.chat_box.see(tk.END)
        self.chat_box.config(state=tk.DISABLED)

    def update_status(self, text, color):
        self.root.after(0, lambda: self.status_lbl.config(text=text, fg=color))

    def start_listening_thread(self):
        threading.Thread(target=self.listen_voice, daemon=True).start()

    def handle_file_upload(self):
        file_path = filedialog.askopenfilename(title="Select System Blueprint")
        if file_path:
            filename = os.path.basename(file_path)
            self.append_chat("BOSS", f"[Processing Data Input: {filename}]")
            self.update_status("Compiling Datasets...", COLOR_BRIGHT)

            def parse_worker():
                reply = f"System blueprint stream payload for {filename} finished parsing, Boss."
                self.append_chat("NOVA", reply)
                nova_os.speak(reply)
                self.update_status("Core Matrix Active", COLOR_BRIGHT)

            threading.Thread(target=parse_worker, daemon=True).start()

    def process_text_input(self):
        user_text = self.text_entry.get().strip()
        if not user_text:
            return

        self.text_entry.delete(0, tk.END)
        self.append_chat("BOSS", user_text)
        self.update_status("Evaluating Matrix...", COLOR_BRIGHT)

        def text_worker():
            reply = nova_os.process_command(user_text)
            self.append_chat("NOVA", reply)
            nova_os.speak(reply)
            self.update_status("Core Matrix Active", COLOR_BRIGHT)
            self.root.after(0, self.realtime_refresh_lists)

        threading.Thread(target=text_worker, daemon=True).start()

    def listen_voice(self):
        r = sr.Recognizer()

        # Audio Tuning Parameters - Lowered baseline to catch quieter inputs
        r.energy_threshold = 100
        r.dynamic_energy_threshold = True
        r.pause_threshold = 1.5

        source = None
        if nova_os.MICROPHONE_DEVICE_INDEX is not None:
            try:
                source = sr.Microphone(device_index=nova_os.MICROPHONE_DEVICE_INDEX)
                with source:
                    pass
            except (OSError, ValueError) as err:
                self.append_chat("SYSTEM", f"Targeted mic index {nova_os.MICROPHONE_DEVICE_INDEX} failed. Error: {err}")
                source = None

        if source is None:
            self.append_chat("SYSTEM", "Attempting System Default Input Capture...")
            try:
                source = sr.Microphone()
                with source:
                    pass
            except Exception as e:
                self.append_chat("SYSTEM", f"Critical: No recording device accessible. Hardware error: {e}")
                self.update_status("Hardware Error", "red")
                return

        with source:
            self.update_status("Awaiting Voice Waveforms...", COLOR_BRIGHT)

            # Print ambient audio calibration specs to monitor line signal noise floors
            try:
                r.adjust_for_ambient_noise(source, duration=0.8)
                self.append_chat("SYSTEM",
                                 f"Calibration done. Ambient noise floor threshold set to: {int(r.energy_threshold)}")
            except Exception as cal_err:
                self.append_chat("SYSTEM", f"Calibration error: {cal_err}")

            try:
                # 12 seconds to begin speaking | 20 seconds maximum phrase runtime
                audio = r.listen(source, timeout=12, phrase_time_limit=20)

                # Check data structure length before making network API requests
                raw_data_len = len(audio.get_raw_data()) if audio else 0
                self.append_chat("SYSTEM", f"Audio payload captured. Raw data size: {raw_data_len} bytes.")

                if raw_data_len < 1000:
                    self.append_chat("SYSTEM",
                                     "Warning: Audio signal is effectively empty. Check microphone connections.")
                    return

                self.update_status("Analyzing Speech Structures...", COLOR_SEA)
                user_input = r.recognize_google(audio, language="en-IN")

                if user_input.strip():
                    self.append_chat("BOSS", user_input)
                    reply = nova_os.process_command(user_input)
                    self.append_chat("NOVA", reply)
                    nova_os.speak(reply)
                else:
                    self.update_status("Empty Signal Detected", COLOR_BRIGHT)

            except sr.WaitTimeoutError:
                self.append_chat("SYSTEM", "Listening window closed: No spoken audio waves detected within 12s.")
            except sr.UnknownValueError:
                self.append_chat("SYSTEM", "Engine Fault: Audio level too faint or distorted to decode.")
            except sr.RequestError as net_err:
                self.append_chat("SYSTEM", f"API connection dropped: {net_err}")
            except Exception as e:
                self.append_chat("SYSTEM", f"Hardware Interface Error: {str(e)}")
            finally:
                self.update_status("Core OS Active", COLOR_BRIGHT)
                self.root.after(0, self.realtime_refresh_lists)

if __name__ == "__main__":
    root = tk.Tk()
    app = NovaOSApp(root)
    root.mainloop()