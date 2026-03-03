# ============================================================
# OLLAMA MODEL CONFIGURATION
# Change model here based on server capacity
# ============================================================

OLLAMA_CONFIG = {

    # Model profiles based on RAM
    "profiles": {

        "mini": {
            "model": "phi3",
            "description": "Fastest, lowest RAM"
        },

        "small": {
            "model": "mistral",
            "description": "Balanced performance"
        },

        "medium": {
            "model": "llama3",
            "description": "High quality"
        },

        "large": {
            "model": "mixtral",
            "description": "Best quality (high RAM)"
        }

    },

    # ACTIVE PROFILE (CHANGE THIS ONLY)
    "active_profile": "mini",

    # OLLAMA SERVER
    "base_url": "http://localhost:11434",

    # GENERATION SETTINGS
    "generation": {
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 800
    }

}


def get_active_model():

    profile = OLLAMA_CONFIG["active_profile"]

    return OLLAMA_CONFIG["profiles"][profile]["model"]