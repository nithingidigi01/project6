# ============================================================
# ULTIMATE AI POST WRITER ENGINE — ENTERPRISE VERSION
# Ollama Powered + Modular Intelligence
# ============================================================

import random

from brand_voice import select_brand_voice
from hashtag_engine import generate_hashtags
from ollama_client import generate_text


# ============================================================
# HOOK ENGINE
# ============================================================

HOOK_PATTERNS = {

    "Authoritative": [
        "Most people misunderstand {topic}.",
        "The truth about {topic} is uncomfortable.",
        "Here’s what professionals won’t tell you about {topic}.",
        "{topic} is not what you think."
    ],

    "Inspirational": [
        "Your journey with {topic} matters more than you think.",
        "If you’re struggling with {topic}, read this.",
        "One day, {topic} will make sense."
    ],

    "Educational": [
        "Let’s break down {topic} in simple terms.",
        "Here’s how {topic} actually works.",
        "A quick guide to understanding {topic}."
    ],

    "Bold": [
        "{topic} is broken.",
        "Unpopular opinion about {topic}.",
        "Nobody wants to admit this about {topic}."
    ],

    "Storytelling": [
        "A few years ago, I learned something about {topic}.",
        "My experience with {topic} changed everything.",
        "This moment taught me about {topic}."
    ]

}


def generate_hook(topic: str, tone: str):

    if tone in HOOK_PATTERNS:
        pattern = random.choice(HOOK_PATTERNS[tone])
    else:
        pattern = "Let’s talk about {topic}."

    return pattern.format(topic=topic)


# ============================================================
# CTA ENGINE
# ============================================================

CTA_PATTERNS = {

    "Professional": [
        "Follow me for more professional insights.",
        "What has your experience been?",
        "Share your thoughts in the comments."
    ],

    "Business": [
        "Follow for more business insights.",
        "What do you think about this?",
        "Let’s discuss."
    ],

    "Personal": [
        "If this resonated, share your thoughts.",
        "You’re not alone in this journey.",
        "What’s your experience?"
    ]

}


def generate_cta(purpose: str):

    if purpose in CTA_PATTERNS:
        return random.choice(CTA_PATTERNS[purpose])

    return "What do you think?"


# ============================================================
# EMOJI ENGINE
# ============================================================

EMOJI_MAP = {

    "Inspirational": ["✨", "🔥", "🚀"],
    "Motivational": ["💪", "🔥", "🚀"],
    "Authoritative": ["📊", "⚡"],
    "Educational": ["📘", "🧠"],
    "Bold": ["⚠️", "🔥"],
    "Storytelling": ["💡", "✨"]

}


def select_emoji(tone: str):

    if tone in EMOJI_MAP:
        return random.choice(EMOJI_MAP[tone])

    return ""


# ============================================================
# PROMPT BUILDER
# ============================================================

def build_ai_prompt(
        purpose: str,
        category: str,
        topic: str,
        tone: str,
        format_type: str,
        brand_voice: str,
        hook: str,
        cta: str,
        emoji: str
):

    return f"""
You are an elite LinkedIn content creator.

Write a high-quality LinkedIn post.

CONTEXT:

Purpose: {purpose}
Category: {category}
Topic: {topic}
Tone: {tone}
Format: {format_type}
Brand Voice: {brand_voice}

HOOK TO START WITH:
{hook}

CTA TO END WITH:
{cta}

Emoji (use naturally if appropriate): {emoji}

WRITING RULES:

- Strong engaging hook (use provided hook)
- Natural human writing
- Clear spacing between lines
- No fluff or generic filler
- Professional but relatable
- High engagement potential
- Match tone and brand voice strictly
- Format based on requested format
- Do NOT include hashtags in body

Generate only the post content.
""".strip()


# ============================================================
# MAIN GENERATION FUNCTION
# ============================================================

def generate_post(
        purpose: str,
        category: str,
        topic: str,
        tone: str,
        format_type: str
):

    # 1️⃣ Brand Voice
    brand_voice = select_brand_voice(
        purpose,
        category,
        topic,
        tone,
        format_type
    )

    # 2️⃣ Hook
    hook = generate_hook(topic, tone)

    # 3️⃣ CTA
    cta = generate_cta(purpose)

    # 4️⃣ Emoji
    emoji = select_emoji(tone)

    # 5️⃣ Build Prompt
    prompt = build_ai_prompt(
        purpose,
        category,
        topic,
        tone,
        format_type,
        brand_voice,
        hook,
        cta,
        emoji
    )

    # 6️⃣ AI Generation via Ollama
    ai_content = generate_text(prompt)

    # 7️⃣ Hashtags
    hashtags = generate_hashtags(
        purpose,
        category,
        topic,
        tone,
        format_type
    )

    hashtag_text = " ".join(hashtags)

    # 8️⃣ Final Post
    final_post = f"""
{ai_content}

{cta} {emoji}

{hashtag_text}
""".strip()

    return {
        "post": final_post,
        "brand_voice": brand_voice,
        "hook": hook,
        "cta": cta,
        "hashtags": hashtags
    }