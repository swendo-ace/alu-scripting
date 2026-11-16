#!/usr/bin/python3
"""Recursively count keywords in the titles of a subreddit's hot posts."""
import collections
import requests


def count_words(subreddit, word_list, after=None, word_count=None):
    """Print a sorted count of keywords found in all hot post titles."""
    if word_count is None:
        word_count = collections.Counter()
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:alu-scripting.api-advanced:v1.0"}
    params = {"after": after, "limit": 100}
    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False, timeout=10)
        if response.status_code != 200:
            return
        data = response.json().get("data", {})
    except Exception:
        return
    titles = map(lambda post: post.get("data", {}).get("title", ""),
                 data.get("children", []))
    word_count.update(" ".join(titles).lower().split())
    after = data.get("after")
    if after is not None:
        return count_words(subreddit, word_list, after, word_count)
    weights = collections.Counter(map(str.lower, word_list))
    scores = map(lambda word: (word, word_count[word] * weights[word]),
                 weights)
    results = sorted(filter(lambda item: item[1] > 0, scores),
                     key=lambda item: (-item[1], item[0]))
    if results:
        print("\n".join(map(lambda item: "{}: {}".format(*item), results)))
