import pytest
from datetime import datetime
from redditide.api_clients.reddit import RedditClient


@pytest.mark.parametrize(
    ("anchor", "expected_posts"),
    [
        (None, ["t3_123", "t3_234", "t3_345"]),
        ("t3_567", ["t3_123", "t3_234", "t3_345", "t3_456", "t3_567"]),
    ],
)
def test_walk_subreddit(httpx_mock, anchor, expected_posts):
    today = datetime.now()
    yesterday = today.replace(day=today.day - 1)

    httpx_mock.add_response(
        json={
            "data": {
                "children": [
                    {
                        "data": {
                            "name": "t3_123",
                            "title": "Post 1",
                            "permalink": "/r/test_subreddit/t3_123/post_1",
                            "created": today.timestamp(),
                        }
                    },
                    {
                        "data": {
                            "name": "t3_234",
                            "title": "Post 2",
                            "permalink": "/r/test_subreddit/t3_234/post_2",
                            "created": today.timestamp(),
                        }
                    },
                    {
                        "data": {
                            "name": "t3_345",
                            "title": "Post 3",
                            "permalink": "/r/test_subreddit/t3_345/post_3",
                            "created": today.timestamp(),
                        }
                    },
                    {
                        "data": {
                            "name": "t3_456",
                            "title": "Post 4",
                            "permalink": "/r/test_subreddit/t3_456/post_4",
                            "created": yesterday.timestamp(),
                        }
                    },
                    {
                        "data": {
                            "name": "t3_567",
                            "title": "Post 5",
                            "permalink": "/r/test_subreddit/t3_567/post_5",
                            "created": yesterday.timestamp(),
                        }
                    },
                ],
                "after": None,
            }
        }
    )

    client = RedditClient()

    posts = client.walk_subreddit("test_subreddit", anchor)

    assert [post.id for post in posts] == expected_posts


@pytest.mark.parametrize(
    ("anchor", "expected_posts"),
    [
        (None, ["t3_123", "t3_234", "t3_345"]),
    ],
)
def test_walk_subreddit_pagination(httpx_mock, anchor, expected_posts):
    today = datetime.now()
    yesterday = today.replace(day=today.day - 1)

    httpx_mock.add_response(
        json={
            "data": {
                "children": [
                    {
                        "data": {
                            "name": "t3_123",
                            "title": "Post 1",
                            "permalink": "/r/test_subreddit/t3_123/post_1",
                            "created": today.timestamp(),
                        }
                    },
                ],
                "after": None,
            }
        }
    )
    httpx_mock.add_response(
        json={
            "data": {
                "children": [
                    {
                        "data": {
                            "name": "t3_234",
                            "title": "Post 2",
                            "permalink": "/r/test_subreddit/t3_234/post_2",
                            "created": today.timestamp(),
                        }
                    },
                ],
                "after": None,
            }
        }
    )
    httpx_mock.add_response(
        json={
            "data": {
                "children": [
                    {
                        "data": {
                            "name": "t3_345",
                            "title": "Post 3",
                            "permalink": "/r/test_subreddit/t3_345/post_3",
                            "created": today.timestamp(),
                        }
                    },
                ],
                "after": None,
            }
        }
    )
    httpx_mock.add_response(
        json={
            "data": {
                "children": [
                    {
                        "data": {
                            "name": "t3_456",
                            "title": "Post 4",
                            "permalink": "/r/test_subreddit/t3_456/post_4",
                            "created": yesterday.timestamp(),
                        }
                    },
                ],
                "after": None,
            }
        }
    )

    client = RedditClient(limit=1)

    posts = client.walk_subreddit("test_subreddit", anchor)

    assert [post.id for post in posts] == expected_posts
