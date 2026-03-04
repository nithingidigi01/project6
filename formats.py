# ============================================================
# MASTER POST FORMAT LIBRARY
# Defines STRUCTURE of content (not tone)
# ============================================================


FORMAT_MASTER = {

    # ========================================================
    # SHORT FORMATS
    # ========================================================

    "Short": {
        "description": "Very concise post. 3–6 lines. Quick insight or message.",
        "use_case": "Fast consumption, frequent posting, simple ideas",
        "structure": [
            "Hook",
            "Key message",
            "Closing thought"
        ]
    },

    "One-Liner": {
        "description": "Single powerful sentence. Maximum impact with minimum words.",
        "use_case": "Quotes, bold opinions, viral thoughts",
        "structure": [
            "One impactful statement"
        ]
    },

    "Quote": {
        "description": "Quote-style post. Statement presented as wisdom or philosophy.",
        "use_case": "Personal brand, inspiration, thought leadership",
        "structure": [
            "Quote line",
            "Optional short explanation"
        ]
    },


    # ========================================================
    # MEDIUM FORMATS
    # ========================================================

    "Standard": {
        "description": "Balanced professional post. 8–15 lines.",
        "use_case": "LinkedIn regular posting",
        "structure": [
            "Hook",
            "Context",
            "Main insight",
            "Conclusion"
        ]
    },

    "List": {
        "description": "Numbered or bullet points sharing tips or ideas.",
        "use_case": "Educational, tips, frameworks",
        "structure": [
            "Hook",
            "Numbered points",
            "Summary"
        ]
    },

    "Tips": {
        "description": "Actionable advice format focused on value delivery.",
        "use_case": "Authority building, educational posts",
        "structure": [
            "Hook",
            "Tips",
            "Encouragement"
        ]
    },

    "Hook + Insight": {
        "description": "Strong opening followed by explanation and insight.",
        "use_case": "Professional thought leadership",
        "structure": [
            "Bold hook",
            "Explanation",
            "Key takeaway"
        ]
    },


    # ========================================================
    # LONG FORMATS
    # ========================================================

    "Long": {
        "description": "Detailed post. 20+ lines. Deep explanation or storytelling.",
        "use_case": "Authority, storytelling, deep insights",
        "structure": [
            "Hook",
            "Context",
            "Story or analysis",
            "Lessons",
            "Conclusion"
        ]
    },

    "Deep Dive": {
        "description": "Analytical or educational deep content with detailed breakdown.",
        "use_case": "Experts, consultants, educators",
        "structure": [
            "Hook",
            "Problem",
            "Detailed analysis",
            "Solution",
            "Takeaways"
        ]
    },


    # ========================================================
    # STORY FORMATS
    # ========================================================

    "Story": {
        "description": "Narrative storytelling format with emotional connection.",
        "use_case": "Personal brand, engagement, relatability",
        "structure": [
            "Situation",
            "Conflict",
            "Turning point",
            "Lesson"
        ]
    },

    "Personal Story": {
        "description": "Real-life experience shared with reflection.",
        "use_case": "Authenticity, trust building",
        "structure": [
            "Personal moment",
            "Challenge",
            "Learning",
            "Advice"
        ]
    },

    "Journey": {
        "description": "Progress over time showing transformation.",
        "use_case": "Career growth, startup journey",
        "structure": [
            "Beginning",
            "Struggles",
            "Growth",
            "Current state"
        ]
    },


    # ========================================================
    # PROFESSIONAL / AUTHORITY
    # ========================================================

    "Thought Leadership": {
        "description": "Opinion-based expert perspective on industry topic.",
        "use_case": "Leaders, founders, professionals",
        "structure": [
            "Bold perspective",
            "Reasoning",
            "Insight",
            "Future view"
        ]
    },

    "Case Study": {
        "description": "Real example explaining problem and solution.",
        "use_case": "Consultants, agencies, experts",
        "structure": [
            "Problem",
            "Approach",
            "Result",
            "Lessons"
        ]
    },

    "Framework": {
        "description": "Structured method or system explanation.",
        "use_case": "Authority building",
        "structure": [
            "Concept",
            "Steps",
            "Application"
        ]
    },


    # ========================================================
    # VIRAL / SOCIAL MEDIA
    # ========================================================

    "Hook + Tips": {
        "description": "Highly engaging viral format with actionable tips.",
        "use_case": "Growth, reach, engagement",
        "structure": [
            "Scroll stopping hook",
            "Tips",
            "CTA"
        ]
    },

    "Myth vs Reality": {
        "description": "Comparison format showing misconception vs truth.",
        "use_case": "Educational, controversial, engaging",
        "structure": [
            "Myth",
            "Reality",
            "Explanation"
        ]
    },

    "Contrarian": {
        "description": "Opposite opinion to common belief.",
        "use_case": "Authority, engagement, bold positioning",
        "structure": [
            "Common belief",
            "Opposite view",
            "Reasoning"
        ]
    },


    # ========================================================
    # EDUCATIONAL
    # ========================================================

    "Guide": {
        "description": "Step-by-step instructional content.",
        "use_case": "Teaching, tutorials",
        "structure": [
            "Goal",
            "Steps",
            "Outcome"
        ]
    },

    "Explainer": {
        "description": "Simplifies complex topic for easy understanding.",
        "use_case": "Education, knowledge sharing",
        "structure": [
            "Concept",
            "Explanation",
            "Example"
        ]
    },

    "Checklist": {
        "description": "Quick reference actionable list.",
        "use_case": "Practical content",
        "structure": [
            "Checklist items"
        ]
    },


    # ========================================================
    # ENGAGEMENT / COMMUNITY
    # ========================================================

    "Question": {
        "description": "Post designed to trigger conversation.",
        "use_case": "Engagement, comments",
        "structure": [
            "Question",
            "Context",
            "Call for opinions"
        ]
    },

    "Poll Style": {
        "description": "Options presented for audience choice.",
        "use_case": "Engagement",
        "structure": [
            "Topic",
            "Options"
        ]
    },

    "Debate": {
        "description": "Two sides of argument presented.",
        "use_case": "Engagement, thought leadership",
        "structure": [
            "Side A",
            "Side B",
            "Your view"
        ]
    },


    # ========================================================
    # PERSONAL BRAND BUILDING
    # ========================================================

    "Lessons": {
        "description": "Learnings from experience.",
        "use_case": "Authority + relatability",
        "structure": [
            "Experience",
            "Lessons",
            "Advice"
        ]
    },

    "Advice": {
        "description": "Direct recommendations to audience.",
        "use_case": "Mentorship tone",
        "structure": [
            "Situation",
            "Advice",
            "Encouragement"
        ]
    },

    "Reflection": {
        "description": "Thoughtful introspection.",
        "use_case": "Deep content",
        "structure": [
            "Observation",
            "Thought",
            "Insight"
        ]
    },


    # ========================================================
    # CAROUSEL / MULTI POST
    # ========================================================

    "Carousel": {
        "description": "Slide-by-slide content for LinkedIn carousel.",
        "use_case": "Visual posts",
        "structure": [
            "Slide hooks",
            "Key points",
            "Conclusion"
        ]
    },

    "Thread": {
        "description": "Multi-post sequence connected together.",
        "use_case": "Deep topics across posts",
        "structure": [
            "Main topic",
            "Multiple parts"
        ]
    },

}