def score_post(text):

    score = 0

    if 400 < len(text) < 1300:
        score += 3

    if "?" in text:
        score += 2

    if "\n\n" in text:
        score += 2

    hashtags = text.count("#")
    if 4 <= hashtags <= 8:
        score += 2

    triggers = [
        "mistake", "truth", "learn", "realize",
        "secret", "change", "growth", "why"
    ]

    if any(t in text.lower() for t in triggers):
        score += 3

    authority = [
        "experience", "results", "worked",
        "professionals", "leaders"
    ]

    if any(a in text.lower() for a in authority):
        score += 2

    return score


def pick_best(posts):

    scored = []

    for p in posts:

        text = p["content"]

        s = score_post(text)

        scored.append((s, p))

    scored.sort(key=lambda x: x[0], reverse=True)

    return scored[0][1]