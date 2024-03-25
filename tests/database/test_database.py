from redditide.api_clients.reddit import Post
from datetime import datetime


def test_insert_and_retrieve(mock_reddit_db):
    mock_reddit_db.insert_post(
        "test_table",
        Post(
            id="123",
            title="title",
            permalink="r/subreddit/comments/id/title",
            created=datetime.now(),
        ),
    )
    post = mock_reddit_db.retrieve_latest_post("test_table")
    assert post == "123"
