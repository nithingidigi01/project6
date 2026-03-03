# ============================================================
# ULTIMATE HASHTAG ENGINE
# Context-Aware Intelligent Hashtag Generation
# ============================================================

import re


# ============================================================
# PURPOSE BASE HASHTAGS
# ============================================================

PURPOSE_TAGS = {

    "Personal": [
        "PersonalGrowth",
        "SelfImprovement",
        "Mindset",
        "LifeLessons",
        "Motivation",
        "Success",
        "Growth",
        "Inspiration",
    ],

    "Professional": [
        "CareerGrowth",
        "ProfessionalDevelopment",
        "Leadership",
        "Skills",
        "WorkLife",
        "Success",
        "Learning",
    ],

    "Business": [
        "Entrepreneurship",
        "BusinessGrowth",
        "Startup",
        "Leadership",
        "Innovation",
        "Success",
        "Strategy",
    ],

}


# ============================================================
# CATEGORY HASHTAGS
# ============================================================

CATEGORY_TAGS = {

    "Software Engineer": [
        "SoftwareEngineering",
        "Developers",
        "Coding",
        "Tech",
        "Programming",
        "TechCareers",
    ],

    "Entrepreneur": [
        "Entrepreneur",
        "Founder",
        "StartupLife",
        "BusinessOwner",
    ],

    "Startup Founder": [
        "Startup",
        "Founders",
        "StartupJourney",
        "BuildInPublic",
    ],

    "Marketing Professional": [
        "Marketing",
        "DigitalMarketing",
        "Branding",
        "ContentMarketing",
    ],

    "Sales Professional": [
        "Sales",
        "SalesSuccess",
        "BusinessDevelopment",
    ],

    "Creator": [
        "ContentCreator",
        "PersonalBrand",
        "CreatorEconomy",
    ],

    "Manager": [
        "Leadership",
        "Management",
        "TeamLeadership",
    ],

    "Freelancer": [
        "Freelancing",
        "RemoteWork",
        "Solopreneur",
    ],

}


# ============================================================
# TONE HASHTAGS
# ============================================================

TONE_TAGS = {

    "Inspirational": [
        "Inspiration",
        "Motivation",
        "Believe",
        "DreamBig",
        "SuccessMindset",
    ],

    "Motivational": [
        "Motivation",
        "Success",
        "Mindset",
        "GrowthMindset",
    ],

    "Authoritative": [
        "Leadership",
        "Expertise",
        "Professional",
        "ThoughtLeadership",
    ],

    "Educational": [
        "Learning",
        "Education",
        "Knowledge",
        "CareerTips",
    ],

    "Bold": [
        "UnpopularOpinion",
        "RealityCheck",
        "Truth",
    ],

    "Analytical": [
        "Insights",
        "Data",
        "Analysis",
    ],

    "Storytelling": [
        "MyJourney",
        "Experience",
        "LessonsLearned",
    ],

}


# ============================================================
# FORMAT HASHTAGS
# ============================================================

FORMAT_TAGS = {

    "Story": ["Story", "Journey", "Experience"],
    "Tips": ["Tips", "Advice", "CareerTips"],
    "Guide": ["Guide", "HowTo"],
    "Quote": ["Quotes", "Wisdom"],
    "Long": ["DeepDive", "Insights"],
    "List": ["Checklist", "KeyPoints"],
}


# ============================================================
# GLOBAL POWER TAGS
# ============================================================

GLOBAL_TAGS = [
    "LinkedIn",
    "Growth",
    "Success",
    "Innovation",
    "Mindset",
    "Career",
    "Business",
    "Leadership",
    "PersonalBrand",
]


# ============================================================
# HELPER
# ============================================================

def clean_tag(text: str):

    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    text = text.replace(" ", "")

    return text


def topic_to_hashtags(topic: str):

    words = topic.split()

    tags = []

    for word in words:
        if len(word) > 2:
            tags.append(clean_tag(word))

    tags.append(clean_tag(topic))

    return tags


# ============================================================
# MAIN ENGINE
# ============================================================

def generate_hashtags(
    purpose: str,
    category: str,
    topic: str,
    tone: str,
    format_type: str,
    max_tags: int = 20
):

    tags = set()

    # Purpose
    if purpose in PURPOSE_TAGS:
        tags.update(PURPOSE_TAGS[purpose])

    # Category
    if category in CATEGORY_TAGS:
        tags.update(CATEGORY_TAGS[category])

    # Tone
    if tone in TONE_TAGS:
        tags.update(TONE_TAGS[tone])

    # Format
    if format_type in FORMAT_TAGS:
        tags.update(FORMAT_TAGS[format_type])

    # Topic derived
    tags.update(topic_to_hashtags(topic))

    # Global tags
    tags.update(GLOBAL_TAGS)

    # Convert to hashtag format
    final_tags = ["#" + clean_tag(tag) for tag in tags]

    # Limit
    return final_tags[:max_tags]