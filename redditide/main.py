from redditide.api_clients.reddit import RedditClient
from redditide.database.reddit import RedditDatabase
from redditide.config import config
from redditide.api_clients.discord import DiscordClient

subreddit = config.get("SUBREDDIT")
channel_id = config.get("CHANNEL_ID")

db = RedditDatabase("reddit.db", subreddit)
client = RedditClient(config.get("LIMIT"))
discord = DiscordClient()

latest_post = db.retrieve_latest_post(subreddit)

if latest_post is not None:
    attempts = 0
    while attempts <= config.get("OFFSET_LIMIT") and client.is_deleted(
        latest_post.permalink
    ):
        attempts += 1
        latest_post = db.retrieve_latest_post(subreddit, offset=attempts)

anchor = latest_post.id if latest_post else None
posts = client.walk_subreddit(subreddit, anchor)

for post in posts:
    db.insert_post(subreddit, post)
    discord.post_to_channel(post, channel_id)
    print(f"{post.title}")
