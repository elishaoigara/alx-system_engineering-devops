#!/usr/bin/python3
"""
Module to recursively query the Reddit API, parse titles,
and count occurrences of given words.
"""
import requests


def count_words(subreddit, word_list, word_count=None, after=None):
    """
    Recursively fetches hot article titles and counts occurrences of words.

    Args:
        subreddit (str): The subreddit to query.
        word_list (list): List of words to count (case-insensitive).
        word_count (dict): Dictionary to store word counts.
        after (str): The 'after' parameter for pagination.

    Returns:
        None (Prints sorted word counts)
    """
    if word_count is None:
        word_count = {}

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "ALX-Reddit-API/1.0"}
    params = {"limit": 100, "after": after}

    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    if response.status_code != 200:
        return

    data = response.json().get("data", {})
    posts = data.get("children", [])

    # Convert word_list to lowercase and remove duplicates
    keywords = set(word.lower() for word in word_list)

    for post in posts:
        title_words = post["data"]["title"].lower().split()

        for word in title_words:
            cleaned_word = ''.join(filter(str.isalpha, word))  # Remove punctuation
            if cleaned_word in keywords:
                word_count[cleaned_word] = word_count.get(cleaned_word, 0) + 1

    after = data.get("after")

    if after:
        return count_words(subreddit, word_list, word_count, after)

    # Sort results: First by count (descending), then alphabetically (ascending)
    sorted_results = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))

    for word, count in sorted_results:
        print(f"{word}: {count}")

