import pytest

from redditide.database.reddit import RedditDatabase


@pytest.fixture
def mock_reddit_db():
    test_db = RedditDatabase(":memory:", "test_table")
    yield test_db
    test_db.close()
