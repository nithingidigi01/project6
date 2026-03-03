# app/redis_state.py

import redis
import os
import json
import time

redis_conn = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    db=0,
    decode_responses=True
)

# ================= JOB STATUS =================

def create_job(job_id, uid):
    redis_conn.hset(f"job:{job_id}", mapping={
        "status": "starting",
        "uid": uid,
        "created_at": int(time.time())
    })

def update_job_status(job_id, status):
    redis_conn.hset(f"job:{job_id}", "status", status)

def get_job_status(job_id):
    data = redis_conn.hgetall(f"job:{job_id}")
    return data.get("status") if data else "unknown"

# ================= UID LOCK =================

def acquire_uid_lock(uid, ttl=600):
    return redis_conn.set(
        f"uid_lock:{uid}",
        "1",
        nx=True,
        ex=ttl
    )

def release_uid_lock(uid):
    redis_conn.delete(f"uid_lock:{uid}")