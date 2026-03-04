import requests
from ollama_config import OLLAMA_CONFIG, get_active_model


def generate_text(prompt: str):

    url = f"{OLLAMA_CONFIG['base_url']}/api/generate"

    payload = {
        "model": get_active_model(),
        "prompt": prompt,
        "stream": False,
        "options": OLLAMA_CONFIG["generation"]
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=300
        )

        if response.status_code != 200:
            raise Exception(response.text)

        data = response.json()
        return data.get("response", "").strip()

    except Exception as e:
        print("Ollama error:", e)
        return (
            "I’ve been reflecting on this lately.\n\n"
            "Growth happens when we question what we think we know.\n\n"
            "What are your thoughts?"
        )