import asyncio
from redditide.api_clients.reddit import RedditClient
from redditide.database.reddit import RedditDatabase
from redditide.config import config

subreddit = config.get("SUBREDDIT")

db = RedditDatabase()
reddit_client = RedditClient(config.get("LIMIT"))


async def main() -> None:
    latest_post = await db.retrieve_latest_post(subreddit)

    if latest_post is not None:
        attempts = 0
        while attempts <= config.get("OFFSET_LIMIT") and reddit_client.is_deleted(
            latest_post.permalink
        ):
            attempts += 1
            latest_post = db.retrieve_latest_post(subreddit, offset=attempts)

    anchor = latest_post.id if latest_post else None
    posts = reddit_client.walk_subreddit(subreddit, anchor)

    tasks = []
    for post in posts:
        tasks.append(db.insert_post(post))
        print(f"{post.title}")
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
