print("🔥 MAIN FILE LOADED")

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import threading
import uuid
from pathlib import Path

from topic_expander import expand_keyword
from ai_writer import generate_post
from linkedin_bot import post_to_linkedin, validate_login

from github_git_storage import (
    prepare_new_uid,
    save_new_profile,
    load_existing_profile,
    cleanup_uid
)

from topic_master import TOPIC_MASTER
from tone_library import TONE_MASTER
from formats import FORMAT_MASTER
from uid_generator import generate_secure_uid


app = FastAPI(title="LinkedIn AI Auto Poster")

BASE_DIR = Path(__file__).resolve().parent

JOB_STATUS = {}
ACTIVE_UIDS = set()
LOCK = threading.Lock()


# ============================================================
# UID GENERATOR
# ============================================================

def generate_uid():
    return generate_secure_uid()


# ============================================================
# REQUEST MODEL
# ============================================================

class PostRequest(BaseModel):
    purpose: str
    category: str
    topic: str
    tone: str
    format_type: str
    unique_id: str | None = None


# ============================================================
# PIPELINE
# ============================================================

def run_pipeline(job_id, data: PostRequest):

    uid = data.unique_id
    state_file = None

    with LOCK:
        if uid in ACTIVE_UIDS:
            JOB_STATUS[job_id] = "already_running"
            return
        ACTIVE_UIDS.add(uid)

    try:

        JOB_STATUS[job_id] = "validating"

        if not uid or not uid.startswith("VIDHWAAN"):
            JOB_STATUS[job_id] = "invalid_uid"
            return

        state_file = load_existing_profile(uid)

        if state_file in ("REPO_NOT_FOUND", "PROFILE_NOT_FOUND", None):
            JOB_STATUS[job_id] = "invalid_uid"
            return

        session_ok = validate_login(False, state_file)

        if not session_ok:
            JOB_STATUS[job_id] = "uid_expired"
            return

        JOB_STATUS[job_id] = "validated"

        topic = expand_keyword(
            data.topic,
            data.category,
            data.purpose,
            data.tone
        )

        result = generate_post(
            data.purpose,
            data.category,
            topic,
            data.tone,
            data.format_type
        )

        post_text = result.get("post", "").strip()

        if not post_text:
            JOB_STATUS[job_id] = "error"
            return

        JOB_STATUS[job_id] = "posting"

        success = post_to_linkedin(post_text, state_file)

        if not success:
            JOB_STATUS[job_id] = "post_failed"
            return

        # ✅ FINAL SUCCESS STATE
        JOB_STATUS[job_id] = "posted"

    except Exception as e:
        print("PIPELINE ERROR:", e)
        JOB_STATUS[job_id] = "error"

    finally:
        try:
            cleanup_uid(uid)
        except Exception as e:
            print("Cleanup error:", e)

        with LOCK:
            ACTIVE_UIDS.discard(uid)

# ============================================================
# API
# ============================================================

@app.post("/generate-post")
def generate_and_post(data: PostRequest):

    if not data.unique_id:
        return {"error": "uid_required"}

    job_id = str(uuid.uuid4())
    JOB_STATUS[job_id] = "starting"

    threading.Thread(
        target=run_pipeline,
        args=(job_id, data),
        daemon=True
    ).start()

    return {
        "job_id": job_id,
        "unique_id": data.unique_id
    }


@app.get("/job-status/{job_id}")
def job_status(job_id: str):
    return {"status": JOB_STATUS.get(job_id, "unknown")}


# ============================================================
# GET UNIQUE ID (LOGIN FLOW)
# ============================================================

@app.post("/get-unique-id")
def get_unique_id():

    uid = generate_uid()

    try:
        state_file = prepare_new_uid(uid)

        # -------- MANUAL LOGIN --------
        login_ok = validate_login(True, str(state_file))

        if not login_ok:
            cleanup_uid(uid)
            return {"status": "login_failed"}

        # -------- SAVE TO GITHUB --------
        save_new_profile(uid, state_file)

        cleanup_uid(uid)

        return {
            "status": "success",
            "unique_id": uid
        }

    except Exception as e:
        cleanup_uid(uid)
        return {
            "status": "error",
            "message": str(e)
        }


# ============================================================
# DROPDOWNS
# ============================================================

@app.get("/api/purposes")
def get_purposes():
    return list(TOPIC_MASTER.keys())


@app.get("/api/categories/{purpose}")
def get_categories(purpose: str):
    return list(TOPIC_MASTER.get(purpose, {}).keys())


@app.get("/api/topics/{purpose}/{category}")
def get_topics(purpose: str, category: str):
    return TOPIC_MASTER.get(purpose, {}).get(category, [])


@app.get("/api/tone-categories")
def get_tone_categories():
    return list(TONE_MASTER.keys())


@app.get("/api/tones/{tone_category}")
def get_tones(tone_category: str):
    return TONE_MASTER.get(tone_category, [])


@app.get("/api/formats")
def get_formats():
    return list(FORMAT_MASTER.keys())


# ============================================================
# FRONTEND
# ============================================================

@app.get("/", response_class=HTMLResponse)
def home():
    file_path = BASE_DIR / "frontend.html"
    return HTMLResponse(file_path.read_text(encoding="utf-8"))