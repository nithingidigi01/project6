# app/tasks.py

from redis_state import (
    update_job_status,
    acquire_uid_lock,
    release_uid_lock
)

from topic_expander import expand_keyword
from ai_writer import generate_post
from linkedin_bot import post_to_linkedin, validate_login
from github_git_storage import load_existing_profile, cleanup_uid

def run_pipeline(job_id, data: dict):

    uid = data["unique_id"]

    if not acquire_uid_lock(uid):
        update_job_status(job_id, "already_running")
        return

    try:

        update_job_status(job_id, "validating")

        if not uid.startswith("VIDHWAAN"):
            update_job_status(job_id, "invalid_uid")
            return

        state_file = load_existing_profile(uid)

        if state_file in ("REPO_NOT_FOUND", "PROFILE_NOT_FOUND", None):
            update_job_status(job_id, "invalid_uid")
            return

        if not validate_login(False, state_file):
            update_job_status(job_id, "uid_expired")
            return

        update_job_status(job_id, "validated")

        topic = expand_keyword(
            data["topic"],
            data["category"],
            data["purpose"],
            data["tone"]
        )

        result = generate_post(
            data["purpose"],
            data["category"],
            topic,
            data["tone"],
            data["format_type"]
        )

        post_text = result.get("post", "").strip()

        if not post_text:
            update_job_status(job_id, "error")
            return

        update_job_status(job_id, "posting")

        if not post_to_linkedin(post_text, state_file):
            update_job_status(job_id, "post_failed")
            return

        update_job_status(job_id, "posted")

    except Exception as e:
        print("WORKER ERROR:", e)
        update_job_status(job_id, "error")

    finally:
        cleanup_uid(uid)
        release_uid_lock(uid)