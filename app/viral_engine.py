import random

VIRAL_HOOKS = [
    "Most people misunderstand this.",
    "Nobody talks about this enough.",
    "This changed how I think completely.",
    "I wish I learned this earlier.",
    "The biggest mistake I see professionals make.",
    "Here’s the truth nobody tells you.",
    "This simple shift creates massive results.",
    "If you’re serious about growth, read this.",
    "This separates average from exceptional.",
    "One insight that changed everything."
]


def generate_hook():
    return random.choice(VIRAL_HOOKS)


def generate_viral_posts(topic, count=5):
    """
    Returns list of post dictionaries:
    [{ "content": "..."}]
    """

    posts = []

    for _ in range(count):

        hook = generate_hook()

        post = f"""{hook}

{topic}

In my experience, the professionals who understand this early gain massive advantage.

Most people wait too long to adapt.

The real question is:
Are you evolving with the industry or staying comfortable?

#AI #Automation #Growth #Leadership
"""

        posts.append({
            "content": post
        })

    return posts