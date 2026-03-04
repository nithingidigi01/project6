from topic_master import TOPIC_MASTER


def choose_from_list(items, title):

    print(f"\nSelect {title}:\n")

    for i, item in enumerate(items, 1):
        print(f"{i}. {item}")

    choice = int(input("\nEnter number: "))

    return items[choice - 1]


def get_user_selection():

    # PURPOSE
    purposes = list(TOPIC_MASTER.keys())

    purpose = choose_from_list(purposes, "Purpose")

    # CATEGORY
    categories = list(TOPIC_MASTER[purpose].keys())

    category = choose_from_list(categories, "Category")

    # TOPIC
    topics = TOPIC_MASTER[purpose][category]

    topic = choose_from_list(topics, "Topic")

    return {
        "purpose": purpose.lower(),
        "category": category,
        "keyword": topic
    }