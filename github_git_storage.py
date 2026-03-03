import requests
from pathlib import Path
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import base64
import shutil

# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
ORG = os.getenv("GITHUB_ORG")
SECRET = os.getenv("PROFILE_SECRET_KEY")

if not TOKEN or not ORG or not SECRET:
    raise RuntimeError("Missing required environment variables")

fernet = Fernet(SECRET.encode())

BASE_DIR = Path(__file__).resolve().parent
RUNTIME_ROOT = BASE_DIR / "runtime_jobs"
RUNTIME_ROOT.mkdir(exist_ok=True)

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

GITHUB_API = "https://api.github.com"


# ============================================================
# INTERNAL HELPERS
# ============================================================

def _repo_url(repo):
    return f"{GITHUB_API}/repos/{ORG}/{repo}"


def _content_url(repo, path):
    return f"{GITHUB_API}/repos/{ORG}/{repo}/contents/{path}"


# ============================================================
# GITHUB OPERATIONS
# ============================================================

def repo_exists(repo: str) -> bool:
    r = requests.get(_repo_url(repo), headers=HEADERS, timeout=20)
    return r.status_code == 200


def create_repo(repo: str):
    """
    Creates repo if not exists.
    Safe to call multiple times.
    """
    r = requests.post(
        f"{GITHUB_API}/orgs/{ORG}/repos",
        headers=HEADERS,
        json={
            "name": repo,
            "private": True,
            "auto_init": True
        },
        timeout=20
    )

    if r.status_code in (201, 202):
        return

    if r.status_code == 422:
        # Already exists
        return

    raise RuntimeError(f"GitHub repo create failed: {r.text}")


def upload_encrypted_state(repo: str, encrypted_bytes: bytes):
    """
    Uploads state.bin (first time only).
    We do NOT update existing files after posting.
    """

    encoded = base64.b64encode(encrypted_bytes).decode()

    r = requests.put(
        _content_url(repo, "state.bin"),
        headers=HEADERS,
        json={
            "message": "initial state upload",
            "content": encoded
        },
        timeout=30
    )

    if r.status_code not in (200, 201):
        raise RuntimeError(f"GitHub upload failed: {r.text}")


def download_encrypted_state(repo: str):
    """
    Downloads encrypted state.bin safely.
    Handles large file edge cases.
    """

    r = requests.get(
        _content_url(repo, "state.bin"),
        headers=HEADERS,
        timeout=20
    )

    if r.status_code == 404:
        return None

    if r.status_code != 200:
        raise RuntimeError(f"GitHub download failed: {r.text}")

    data = r.json()

    # GitHub returns encoding: none if file too large
    if data.get("encoding") != "base64":
        # Use raw download_url instead
        download_url = data.get("download_url")
        if not download_url:
            return None

        raw = requests.get(download_url, timeout=30)
        if raw.status_code != 200:
            raise RuntimeError("Raw download failed")
        return raw.content

    content = data["content"].replace("\n", "")
    return base64.b64decode(content)


# ============================================================
# UID FLOW
# ============================================================

def prepare_new_uid(uid: str) -> Path:
    """
    Creates local runtime folder for new UID login.
    Returns storage_state.json path.
    """

    uid_root = RUNTIME_ROOT / uid
    uid_root.mkdir(parents=True, exist_ok=True)

    return uid_root / "storage_state.json"


def save_new_profile(uid: str, state_file: Path):
    """
    Called ONLY after successful manual login.
    Encrypts and uploads state to GitHub.
    """

    if not state_file.exists():
        raise RuntimeError("storage_state.json not found")

    encrypted = fernet.encrypt(state_file.read_bytes())

    create_repo(uid)
    upload_encrypted_state(uid, encrypted)


def load_existing_profile(uid: str):
    """
    Downloads and decrypts stored session.
    Returns path to local storage_state.json
    """

    if not repo_exists(uid):
        return "REPO_NOT_FOUND"

    encrypted = download_encrypted_state(uid)

    if not encrypted:
        return "PROFILE_NOT_FOUND"

    uid_root = RUNTIME_ROOT / uid
    uid_root.mkdir(parents=True, exist_ok=True)

    state_file = uid_root / "storage_state.json"

    try:
        decrypted = fernet.decrypt(encrypted)
    except Exception:
        return "PROFILE_CORRUPTED"

    state_file.write_bytes(decrypted)

    return str(state_file)


def cleanup_uid(uid: str):
    """
    Removes local runtime folder.
    Never touches GitHub.
    """

    uid_root = RUNTIME_ROOT / uid
    if uid_root.exists():
        shutil.rmtree(uid_root, ignore_errors=True)