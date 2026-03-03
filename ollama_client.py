# ============================================================
# SMART OLLAMA CLIENT
# Auto-detect installed models + keyword matching
# ============================================================

import requests
import subprocess
from ollama_config import OLLAMA_CONFIG, get_active_model


# ============================================================
# GET INSTALLED MODELS
# ============================================================

def get_installed_models():

    try:

        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True
        )

        lines = result.stdout.splitlines()[1:]

        models = [line.split()[0] for line in lines if line.strip()]

        return models

    except Exception:
        return []


# ============================================================
# RESOLVE MODEL NAME
# ============================================================

def resolve_model(requested_model):

    installed = get_installed_models()

    if not installed:
        return requested_model

    # Exact match
    if requested_model in installed:
        return requested_model

    # Keyword match (phi3 → phi3:mini)
    for model in installed:
        if model.startswith(requested_model):
            return model

    # Fallback first installed
    return installed[0]


# ============================================================
# GENERATE TEXT
# ============================================================

def generate_text(prompt: str):

    url = f"{OLLAMA_CONFIG['base_url']}/api/generate"

    requested_model = get_active_model()

    model = resolve_model(requested_model)

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": OLLAMA_CONFIG["generation"]
    }

    try:

        print(f"[AI] Using model: {model}")

        response = requests.post(
            url,
            json=payload,
            timeout=300
        )

        if response.status_code != 200:
            raise Exception(response.text)

        data = response.json()

        text = data.get("response", "").strip()

        if text:
            return text

    except Exception as e:

        print("Primary model failed:", e)

        # Fallback attempt
        try:

            installed = get_installed_models()

            if installed:
                fallback_model = installed[0]

                print(f"[AI] Fallback model: {fallback_model}")

                payload["model"] = fallback_model

                response = requests.post(url, json=payload, timeout=300)

                data = response.json()

                text = data.get("response", "").strip()

                if text:
                    return text

        except Exception as e2:
            print("Fallback failed:", e2)

    return fallback_text()


# ============================================================
# FALLBACK
# ============================================================

def fallback_text():

    return (
        "I’ve been thinking about this a lot lately.\n\n"
        "Sometimes the biggest insights come from simple realizations.\n\n"
        "Growth happens when we question what we think we know."
    )