import random


# =========================
# VIRAL PSYCHOLOGY PATTERNS
# =========================

CURIOSITY_PATTERNS = [
    "What nobody tells you about {}",
    "The truth about {}",
    "What most people misunderstand about {}",
    "Why {} is more important than you think",
]

CONTRARIAN_PATTERNS = [
    "Why most people are wrong about {}",
    "The biggest misconception about {}",
    "Stop believing this about {}",
    "The uncomfortable truth about {}",
]

FUTURE_PATTERNS = [
    "The future of {}",
    "Why {} will dominate the next decade",
    "How {} is changing everything",
    "Where {} is heading next",
]

MISTAKE_PATTERNS = [
    "A mistake people make about {}",
    "The biggest mistake in {}",
    "Why people fail at {}",
    "Common mistakes in {} nobody talks about",
]

SUCCESS_PATTERNS = [
    "How {} creates real success",
    "Lessons from {}",
    "How {} changed my perspective",
    "What I learned from {}",
]

INSIGHT_PATTERNS = [
    "Understanding {} in today's world",
    "The hidden power of {}",
    "The real impact of {}",
    "Why {} matters more than ever",
]

ALL_PATTERNS = (
    CURIOSITY_PATTERNS
    + CONTRARIAN_PATTERNS
    + FUTURE_PATTERNS
    + MISTAKE_PATTERNS
    + SUCCESS_PATTERNS
    + INSIGHT_PATTERNS
)


# =========================
# PURPOSE CONTEXT BOOSTER
# =========================

def purpose_modifier(topic: str, purpose: str) -> str:

    if purpose == "personal":

        modifiers = [
            f"My personal experience with {topic}",
            f"What {topic} taught me about life",
            f"A perspective on {topic} that changed me",
        ]

    elif purpose == "professional":

        modifiers = [
            f"What professionals should know about {topic}",
            f"A professional perspective on {topic}",
            f"How {topic} impacts careers today",
        ]

    elif purpose == "business":

        modifiers = [
            f"What business leaders should know about {topic}",
            f"How {topic} affects business growth",
            f"A strategic view on {topic}",
        ]

    else:
        return topic

    # 30% chance to enhance
    if random.random() < 0.3:
        return random.choice(modifiers)

    return topic


# =========================
# CATEGORY CONTEXT BOOSTER
# =========================

def category_modifier(topic: str, category: str) -> str:

    # Adds domain clarity for unlimited categories
    if category:

        if random.random() < 0.35:

            return f"{topic} in {category}"

    return topic


# =========================
# HOOK INTENSIFIER
# =========================

def intensify(topic: str) -> str:

    intensifiers = [
        topic,
        f"Why {topic}",
        f"The reality of {topic}",
        f"The problem with {topic}",
        f"The opportunity in {topic}",
    ]

    return random.choice(intensifiers)


# =========================
# MAIN EXPANDER
# =========================

# =========================
# MAIN EXPANDER
# =========================

def expand_keyword(keyword: str, category=None, purpose=None, tone=None):

    # Step 1 — Base topic
    base_topic = keyword.strip()

    # Step 2 — Category context
    base_topic = category_modifier(base_topic, category)

    # Step 3 — Purpose context
    base_topic = purpose_modifier(base_topic, purpose)

    # Optional tone influence (future extensibility)
    # Currently not changing logic but keeps compatibility
    if tone:
        pass

    # Step 4 — Intensify
    base_topic = intensify(base_topic)

    # Step 5 — Viral pattern
    pattern = random.choice(ALL_PATTERNS)

    final_topic = pattern.format(base_topic)

    return final_topic