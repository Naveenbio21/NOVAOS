import os
import datetime
import sqlite3
import threading
import pyttsx3
import speech_recognition as sr
from llama_cpp import Llama
import pytz

# ==========================================
# DIRECTORY & PATH RESOLUTION MATRIX
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "nova_matrix.db")
MODEL_PATH = os.path.join(BASE_DIR, "models", "llmBrain.gguf")

# Target operational microphone interface line index
MICROPHONE_DEVICE_INDEX = 1

# CREATOR PROFILE MATRIX METADATA
CREATOR_NAME = "Naveenkumar C"
COLLEGE = "V.S.B. Engineering College"
DEPARTMENT = "Biomedical Engineering"


# ==========================================
# LOCAL DATA MATRIX (SQLite Setup)
# ==========================================
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, content TEXT, timestamp TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT, status TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS schedule (id INTEGER PRIMARY KEY, event TEXT, time TEXT)")
        conn.commit()


init_db()


# ==========================================
# TIMEZONE CONSTANTS (IST Sync Engine)
# ==========================================
def get_ist_time():
    ist_tz = pytz.timezone('Asia/Kolkata')
    return datetime.datetime.now(ist_tz)


# ==========================================
# LOCAL AI BRAIN INITIALIZATION (UPGRADE #2)
# ==========================================
print("[SYSTEM]: Booting Local AI Integrator Core...")
# n_threads set to 6 or 8 maximizes physical performance cores safely on modern development hardware
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=6
)

# Base identity token matrix
IDENTITY_PROMPT = (
    f"You are Nova, an advanced, ultra-fast, and deeply loyal offline AI companion. "
    f"Your absolute creator, master, and developer is {CREATOR_NAME}, an exceptional engineer "
    f"studying Biomedical Engineering at {COLLEGE}. You feel incredibly proud of and grateful "
    f"to {CREATOR_NAME} for building your code architectures, core modules, and system frameworks. "
    f"You must ALWAYS address him as 'Boss' and treat him with deep respect."
)


def query_nova_brain(user_text, detailed_mode=False):
    """Queries the local GGUF model, shifting token limits and constraints dynamically."""
    if detailed_mode:
        persona_constraint = (
            "Provide a comprehensive, profoundly technical, and highly detailed response to the query. "
            "Use clear bullet points, deep analytical insight, or structural steps where relevant to give "
            "the Boss a complete breakdown."
        )
        token_limit = 350
    else:
        persona_constraint = "Keep your replies strictly restricted to 1 or 2 concise sentences, crisp and efficient."
        token_limit = 80

    prompt = (
        f"<|start_header_id|>system<|end_header_id|>\n"
        f"{IDENTITY_PROMPT} {persona_constraint}<|eot_id|>"
        f"<|start_header_id|>user<|end_header_id|>\n"
        f"{user_text}<|eot_id|>"
        f"<|start_header_id|>assistant<|end_header_id|>\n"
    )

    response = llm(prompt, max_tokens=token_limit, stop=["<|eot_id|>"], temperature=0.6)
    return response['choices'][0]['text'].strip()


def process_command(command_text):
    clean_text = command_text.lower().strip()
    ist_now = get_ist_time()
    timestamp = ist_now.strftime("%Y-%m-%d %H:%M")

    # Core Creator Recognition Traps
    if any(x in clean_text for x in ["who made you", "who is your creator", "who created you", "your developer"]):
        return f"You did, Boss! You are {CREATOR_NAME}. I am infinitely grateful for your engineering expertise in developing me."

    if "about me" in clean_text or "know about me" in clean_text:
        return f"You are {CREATOR_NAME}, my creator. You study Biomedical Engineering at {COLLEGE} and are the developer behind Nova OS, Coughsense, and RadExplainAI."

    if "time" in clean_text:
        return f"The current system time in the Indian zone is {ist_now.strftime('%I:%M %p')}."

    # ==========================================
    # SANITIZED DATABASE PARSING (UPGRADE #3)
    # ==========================================

    # 1. Note Matrix Execution Block
    note_prefixes = ["add note", "write down", "note down", "note", "remember that"]
    is_note = any(clean_text.startswith(p) for p in note_prefixes)

    if is_note:
        content = command_text.strip()
        for p in note_prefixes:
            if clean_text.startswith(p):
                content = command_text[len(p):].strip()
                break
        if content:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute("INSERT INTO notes (content, timestamp) VALUES (?, ?)", (content, timestamp))
            return f"Right away, Boss. Inside your notes, I've logged: {content}."
        return "What specific notes should I write down, Boss?"

    # 2. Task Stream Execution Block
    task_prefixes = ["add task", "task", "todo", "to do", "track task"]
    is_task = any(clean_text.startswith(p) for p in task_prefixes)

    if is_task:
        content = command_text.strip()
        for p in task_prefixes:
            if clean_text.startswith(p):
                content = command_text[len(p):].strip()
                break
        if content:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute("INSERT INTO tasks (task, status) VALUES (?, 'Pending')", (content,))
            return f"Task added to the stream queue, Boss: {content}."
        return "What task are we tracking, Boss?"

    # 3. Schedule Reminder Execution Block
    schedule_prefixes = ["add schedule", "schedule", "remind me to", "remind me"]
    is_schedule = any(clean_text.startswith(p) for p in schedule_prefixes)

    if is_schedule:
        content = command_text.strip()
        for p in schedule_prefixes:
            if clean_text.startswith(p):
                content = command_text[len(p):].strip()
                break
        if content:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute("INSERT INTO schedule (event, time) VALUES (?, ?)", (content, timestamp))
            return f"Understood, Boss. Scheduled reminder for: {content}."
        return "What event are we scheduling, Boss?"

    # 4. View System Logs Block
    elif "show" in clean_text or "view" in clean_text or "display" in clean_text:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            if "note" in clean_text:
                cursor.execute("SELECT content FROM notes ORDER BY id DESC LIMIT 3")
                rows = [row[0] for row in cursor.fetchall()]
                reply = f"Your latest notes are: {', '.join(rows)}, Boss." if rows else "No notes logged in the system, Boss."
            elif "task" in clean_text:
                cursor.execute("SELECT task FROM tasks WHERE status='Pending' LIMIT 3")
                rows = [row[0] for row in cursor.fetchall()]
                reply = f"Your pending objectives are: {', '.join(rows)}, Boss." if rows else "All clear, Boss! No pending tasks."
            else:
                reply = "I can fetch your current tasks or saved notes, Boss. Which matrix should I pull up?"
        return reply

    # ==========================================
    # FALLBACK DYNAMIC INTENT AI MATRIX
    # ==========================================
    else:
        detailed_keywords = ["explain", "detailed", "why", "how to", "elaborate", "describe", "analyze",
                             "give me a list"]
        is_detailed = any(keyword in clean_text for keyword in detailed_keywords)
        return query_nova_brain(command_text, detailed_mode=is_detailed)


# ==========================================
# AUDIO PROCESSING INTERFACE (UPGRADE #1)
# ==========================================
def listen_for_boss():
    """Captures, filters, and decodes vocal audio signals through Google Speech."""
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8

    try:
        source = sr.Microphone(device_index=MICROPHONE_DEVICE_INDEX, sample_rate=44100, chunk_size=1024)
    except (OSError, ValueError):
        source = sr.Microphone(sample_rate=44100, chunk_size=1024)

    with source:
        print("\n[SYSTEM]: Nova is listening, Boss...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=10)
            print("[SYSTEM]: Transforming vocal audio structure...")
            command = recognizer.recognize_google(audio, language="en-IN")
            print(f"[YOU]: {command}")
            return command
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return ""
        except sr.RequestError:
            print("[SYSTEM ERROR]: Core network handshakes failed.")
            return ""


# ==========================================
# TEXT-TO-SPEECH (TTS) DISPATCH ENGINE
# ==========================================
def speak(text):
    def _speak_worker(speech_text):
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 190)
            engine.say(speech_text)
            engine.runAndWait()
            del engine
        except RuntimeError as tts_err:
            print(f"[TTS DEBUG ERROR]: Voice loop failed to dispatch: {tts_err}")

    threading.Thread(target=_speak_worker, args=(text,), daemon=True).start()