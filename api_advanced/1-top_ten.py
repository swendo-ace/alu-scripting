#!/usr/bin/python3
"""Print the titles of the first 10 hot posts for a given subreddit."""
import requests


def top_ten(subreddit):
    """Print the titles of the 10 hottest posts, or None if invalid."""
    url = "https://www.reddit.com/r/{}/hot.json?limit=10".format(subreddit)
    headers = {"User-Agent": "linux:alu-scripting.api-advanced:v1.0"}
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code != 200:
        print(None)
        return
    posts = response.json().get("data", {}).get("children", [])
    for post in posts:
        print(post.get("data", {}).get("title"))
