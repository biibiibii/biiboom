from pydantic import BaseSettings

from app.log_handler import LogHandler


class Settings(BaseSettings):
    log_name = "etl"
    log_level = "INFO"
    mongodb_database = "news_spider"
    mongodb_host = "127.0.0.1"
    mongodb_port = 27017
    mongodb_username = "root"
    mongodb_password = "root"
    mysql_ip = "127.0.0.1"
    mysql_port = 3306
    mysql_db = "news_spider"
    mysql_user_name = "root"
    mysql_user_pass = "root"
    redisdb_ip_ports = "127.0.0.1:6379"
    redisdb_user_pass = ""

    max_thread_count = 3

    forum_urls = [
        "https://forum.bnbchain.org",
        "https://ethereum-magicians.org",
        "https://forum.cosmos.network",
        "https://forum.polkadot.network",
        "https://gov.near.org",
        "https://forum.aptoslabs.com",
        "https://forum.astar.network",
        "https://forum.avax.network",
        "https://research.arbitrum.io",
        "https://forum.polygon.technology",
        "https://gov.optimism.io",
        "https://forums.sui.io",
        "https://forums.sui.io",
        "https://forum.dfinity.org",
    ]


settings = Settings()
logger = LogHandler(settings.log_name, settings.log_level)
