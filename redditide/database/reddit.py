from prisma import Prisma
from prisma.models import Post


class RedditDatabase:
    def __init__(self) -> None:
        self.db = Prisma()

    async def insert_post(self, post: Post) -> None:
        if not self.db.is_connected():
            await self.db.connect()

        await self.db.post.create(
            {
                "id": post.id,
                "subreddit": post.subreddit,
                "title": post.title,
                "permalink": post.permalink,
                "created": post.created,
            },
        )

    # create_many is not available for SQLite
    async def insert_posts(self, posts: list[Post]) -> None:
        if not self.db.is_connected():
            await self.db.connect()

        await self.db.post.create_many(
            [
                {
                    "id": post.id,
                    "subreddit": post.subreddit,
                    "title": post.title,
                    "permalink": post.permalink,
                    "created": post.created,
                }
                for post in posts
            ]
        )

    async def retrieve_latest_post(
        self, subreddit: str, offset: int = 0
    ) -> Post | None:
        if not self.db.is_connected():
            await self.db.connect()

        post = await self.db.post.find_first(
            skip=offset, order={"created": "desc"}, where={"subreddit": subreddit}
        )

        if post is None:
            return None

        return Post(
            id=post.id,
            subreddit=post.subreddit,
            title=post.title,
            permalink=post.permalink,
            created=post.created,
        )

    async def close(self) -> None:
        await self.db.disconnect()
