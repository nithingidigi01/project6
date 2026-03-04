print("🔥 MAIN FILE LOADED")

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uuid
from pathlib import Path
import redis
from rq import Queue

from redis_state import create_job, get_job_status
from tasks import run_pipeline

from github_git_storage import (
    prepare_new_uid,
    save_new_profile,
    cleanup_uid
)

from topic_master import TOPIC_MASTER
from tone_library import TONE_MASTER
from formats import FORMAT_MASTER
from uid_generator import generate_secure_uid
from linkedin_bot import validate_login


# ============================================================
# APP INIT
# ============================================================

app = FastAPI(title="LinkedIn AI Auto Poster")

BASE_DIR = Path(__file__).resolve().parent

redis_conn = redis.Redis(
    host="redis",
    port=6379,
    db=0,
    decode_responses=True
)

queue = Queue("linkedin", connection=redis_conn)


# ============================================================
# REQUEST MODEL
# ============================================================

class PostRequest(BaseModel):
    purpose: str
    category: str
    topic: str
    tone: str
    format_type: str
    unique_id: str


# ============================================================
# GENERATE & POST (QUEUE ENTRY)
# ============================================================

@app.post("/generate-post")
def generate_and_post(data: PostRequest):

    job_id = str(uuid.uuid4())

    # Create job in Redis
    create_job(job_id, data.unique_id)

    # Enqueue worker job
    queue.enqueue(
        run_pipeline,
        job_id,
        data.dict(),
        job_timeout=900
    )

    return {
        "job_id": job_id,
        "unique_id": data.unique_id
    }


# ============================================================
# JOB STATUS
# ============================================================

@app.get("/job-status/{job_id}")
def job_status(job_id: str):
    return {"status": get_job_status(job_id)}


# ============================================================
# UNIQUE ID FLOW
# ============================================================

@app.post("/get-unique-id")
def get_unique_id():

    uid = generate_secure_uid()

    try:
        state_file = prepare_new_uid(uid)

        login_ok = validate_login(True, str(state_file))

        if not login_ok:
            cleanup_uid(uid)
            return {"status": "login_failed"}

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
    return HTMLResponse(
        (BASE_DIR / "frontend.html").read_text(encoding="utf-8")
    )