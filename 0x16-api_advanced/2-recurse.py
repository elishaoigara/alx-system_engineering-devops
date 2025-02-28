#!/usr/bin/python3
"""
Module to recursively query the Reddit API and return hot article titles.
"""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """
    Recursively fetches hot article titles for a given subreddit.

    Args:
        subreddit (str): The subreddit to query.
        hot_list (list): A list to store article titles (default: []).
        after (str): The 'after' parameter for pagination.

    Returns:
        list: A list containing the titles of all hot articles.
        None: If the subreddit is invalid.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "ALX-Reddit-API/1.0"}
    params = {"limit": 100, "after": after}

    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    if response.status_code != 200:
        return None

    data = response.json().get("data", {})
    posts = data.get("children", [])

    for post in posts:
        hot_list.append(post["data"]["title"])

    after = data.get("after")

    if after:
        return recurse(subreddit, hot_list, after)

    return hot_list

