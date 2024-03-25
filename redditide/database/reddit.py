import sqlite3

from redditide.api_clients.reddit import Post


class RedditDatabase:
    def __init__(self, db_name: str, table_name: str) -> None:
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_table(table_name)

    def _create_table(self, table_name: str) -> None:
        sanitized_table_name = table_name.replace("'", "''")
        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {sanitized_table_name}
                                   (id TEXT, title TEXT, permalink TEXT, created INTEGER)"""
        )
        self.conn.commit()

    def insert_post(self, table_name: str, post: Post) -> None:
        sanitized_table_name = table_name.replace("'", "''")
        self.cursor.execute(
            f"INSERT INTO {sanitized_table_name} (id, title, permalink, created) VALUES (?, ?, ?, ?)",
            (post.id, post.title, post.permalink, post.created),
        )
        self.conn.commit()

    def retrieve_latest_post(self, table_name: str, offset: int = 0) -> Post | None:
        sanitized_table_name = table_name.replace("'", "''")
        self.cursor.execute(
            f"SELECT * FROM {sanitized_table_name} ORDER BY created DESC LIMIT 1 OFFSET {offset}"
        )
        result = self.cursor.fetchone()
        if result:
            return Post(
                id=result["id"],
                title=result["title"],
                permalink=result["permalink"],
                created=result["created"],
            )
        return None

    def close(self) -> None:
        self.conn.close()
