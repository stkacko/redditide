import httpx

from datetime import datetime
from dataclasses import dataclass
import os


@dataclass
class Post:
    id: str
    title: str
    permalink: str
    created: datetime
    author: str  # TODO: get user avatar in front of username and add link https://www.reddit.com/user/DigitalSplendid/about.json
    selftext: str
    link_flair_text: str | None
    # url_overridden_by_dest: str  # if url then insert into post
    url: str


class RedditClient:
    client: httpx.Client
    limit: int
    max_posts_subreddit: int

    def __init__(self, limit: int = 100, max_posts_subreddit: int = 10000) -> None:
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")

        self.limit = limit
        self.max_posts_subreddit = max_posts_subreddit
        self.client = httpx.Client(
            base_url="https://www.reddit.com",
            headers={
                "User-Agent": "redditbot/0.1 (by /u/stkftw)",
                "Authorization": f"Basic {client_id}:{client_secret}",
            },
        )

    def is_deleted(self, permalink: str) -> bool:
        response = self.client.get(f"{permalink}.json")
        if response.json()[0]["data"]["children"][0]["data"]["removed_by_category"]:
            return True
        return False

    def walk_subreddit(self, name: str, anchor: str | None = None) -> list[Post]:
        today = datetime.now().date()

        result = []
        posts_fetched = 0

        params = {"limit": self.limit}
        if anchor:
            params["before"] = anchor

        done = False

        while not done and posts_fetched < self.max_posts_subreddit:
            response = self.client.get(f"/r/{name}/new.json", params=params)

            if response.status_code != 200:
                raise Exception(f"Error fetching posts: {response.status_code}")

            posts = response.json()["data"]["children"]
            if not posts:
                break

            for post in posts:
                postobj = Post(
                    id=post["data"]["name"],
                    title=post["data"]["title"],
                    permalink=post["data"]["permalink"],
                    created=datetime.fromtimestamp(post["data"]["created"]),
                    author=post["data"]["author"],
                    selftext=post["data"]["selftext"],
                    link_flair_text=post["data"]["link_flair_text"],
                    # url_overridden_by_dest=post["data"].get("url_overridden_by_dest"),
                    url=post["data"]["url"],
                )

                # this is the first time the subreddit is scraped, there's no reference
                # fetch all the posts for today
                if not anchor and postobj.created.date() != today:
                    done = True
                    break

                result.append(postobj)

            if len(posts) < self.limit:
                break

            if not anchor:
                params["after"] = response.json()["data"]["after"]
                continue

            # in this case there's a reference, so we need to scrape all posts
            # until that anchor is reached, so we can't use the after parameter
            # we need to use the before parameter + count to skip the posts we already have read

            params["before"] = posts[0]["data"]["name"]
            # params["count"] = posts_fetched = len(result)
            posts_fetched = len(result)

        return sorted(result, key=lambda post: post.created, reverse=True)
