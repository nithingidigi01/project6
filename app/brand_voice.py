# ============================================================
# ULTIMATE BRAND VOICE ENGINE
# Stateless — No User Storage Required
# ============================================================


# ============================================================
# BRAND VOICE DEFINITIONS
# ============================================================

BRAND_VOICES = {

    "Authority Leader": {
        "description": "Confident expert positioning with clarity and authority",
        "style": "confident, professional, decisive"
    },

    "Inspirational Coach": {
        "description": "Motivational and uplifting guidance",
        "style": "encouraging, positive, energetic"
    },

    "Friendly Mentor": {
        "description": "Supportive and relatable communication",
        "style": "warm, helpful, conversational"
    },

    "Visionary Leader": {
        "description": "Future-focused strategic thinking",
        "style": "bold, forward-thinking, innovative"
    },

    "Bold Challenger": {
        "description": "Provocative and opinionated perspective",
        "style": "direct, fearless, challenging"
    },

    "Analytical Expert": {
        "description": "Logical and data-driven explanation",
        "style": "structured, precise, logical"
    },

    "Storyteller": {
        "description": "Narrative-driven human connection",
        "style": "engaging, emotional, relatable"
    },

    "Educator": {
        "description": "Teaching and knowledge sharing",
        "style": "clear, structured, informative"
    },

    "Corporate Executive": {
        "description": "Formal leadership communication",
        "style": "strategic, polished, executive"
    },

    "Personal Brand Authority": {
        "description": "Strong positioning and influence building",
        "style": "confident, authentic, influential"
    },

}



# ============================================================
# PURPOSE DEFAULT VOICES
# ============================================================

PURPOSE_DEFAULT = {

    "Personal": "Friendly Mentor",
    "Professional": "Authority Leader",
    "Business": "Visionary Leader"

}


# ============================================================
# TONE PRIORITY MAPPING
# Tone overrides purpose when strong signal exists
# ============================================================

TONE_TO_VOICE = {

    # Authority
    "Authoritative": "Authority Leader",
    "Professional": "Authority Leader",
    "Executive": "Corporate Executive",

    # Inspiration
    "Inspirational": "Inspirational Coach",
    "Motivational": "Inspirational Coach",

    # Education
    "Educational": "Educator",
    "Guide": "Educator",
    "Teaching": "Educator",

    # Bold
    "Bold": "Bold Challenger",
    "Controversial": "Bold Challenger",
    "Provocative": "Bold Challenger",

    # Analytical
    "Analytical": "Analytical Expert",
    "Data Driven": "Analytical Expert",

    # Story
    "Storytelling": "Storyteller",
    "Personal": "Storyteller",

    # Vision
    "Visionary": "Visionary Leader",
    "Future": "Visionary Leader",

    # Casual
    "Friendly": "Friendly Mentor",
    "Conversational": "Friendly Mentor",

}


# ============================================================
# FORMAT ADJUSTMENT (Optional refinement)
# ============================================================

FORMAT_HINT = {

    "Story": "Storyteller",
    "Personal Story": "Storyteller",
    "Case Study": "Analytical Expert",
    "Thought Leadership": "Authority Leader",
    "Guide": "Educator",
    "Quote": "Personal Brand Authority"

}


# ============================================================
# MAIN SELECTION ENGINE
# ============================================================

def select_brand_voice(
    purpose: str,
    category: str,
    topic: str,
    tone: str,
    format_type: str
):

    # 1️⃣ Tone has highest priority
    if tone in TONE_TO_VOICE:
        return TONE_TO_VOICE[tone]

    # 2️⃣ Format refinement
    if format_type in FORMAT_HINT:
        return FORMAT_HINT[format_type]

    # 3️⃣ Purpose default
    if purpose in PURPOSE_DEFAULT:
        return PURPOSE_DEFAULT[purpose]

    # 4️⃣ Fallback
    return "Personal Brand Authority"