#!/usr/bin/python3
"""Recursively collect the titles of all hot posts for a subreddit."""
import requests


def recurse(subreddit, hot_list=None, after=None):
    """Return a list of all hot post titles, or None if invalid."""
    if hot_list is None:
        hot_list = []
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:alu-scripting.api-advanced:v1.0"}
    params = {"after": after, "limit": 100}
    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False, timeout=10)
        if response.status_code != 200:
            return None
        data = response.json().get("data", {})
    except Exception:
        return None
    hot_list.extend(map(lambda post: post.get("data", {}).get("title"),
                        data.get("children", [])))
    after = data.get("after")
    if after is None:
        return hot_list if hot_list else None
    return recurse(subreddit, hot_list, after)
