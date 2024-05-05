import os

import httpx

from redditide.api_clients.reddit import Post


class DiscordClient:
    client: httpx.Client

    def __init__(self) -> None:
        bot_token = os.getenv("BOT_TOKEN")

        self.client = httpx.Client(
            base_url="https://discord.com",
            headers={
                "Authorization": f"Bot {bot_token}",
                "Content-Type": "application/json",
            },
        )

    def post_to_channel(self, post: Post, channel_id: str) -> None:
        # TODO: build elsewhere?
        embed = {
                "author": {
                    "name": post.author,
                    # "icon_url": "TBD",
                    "url": f"https://www.reddit.com/u/{post.author}"
                },
                "title": f"{post.title} - {post.link_flair_text}",
                "url": f"https://www.reddit.com{post.permalink}",
                "description": post.selftext,
                "image": {
                    "url": post.url,
                },
        }

        response = self.client.post(
            f"/api/channels/{channel_id}/messages", json={"embed": embed}
        )

        # if response.status_code == 200:
        #     print("kekw")
