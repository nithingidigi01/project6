OLLAMA_CONFIG = {

    "profiles": {
        "mini": {
            "model": "phi3:mini",
            "description": "Fastest, lowest RAM"
        }
    },

    "active_profile": "mini",

    # IMPORTANT: Docker service name
    "base_url": "http://ollama:11434",

    "generation": {
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 800
    }
}


def get_active_model():
    profile = OLLAMA_CONFIG["active_profile"]
    return OLLAMA_CONFIG["profiles"][profile]["model"]