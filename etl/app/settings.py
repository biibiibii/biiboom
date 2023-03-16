from pydantic import BaseSettings

from app.log_handler import LogHandler


class Settings(BaseSettings):
    log_name = "etl"
    log_level = "INFO"

    mysql_ip = "127.0.0.1"
    mysql_port = 3305
    mysql_db = "news_spider"
    mysql_user_name = "root"
    mysql_user_pass = "root"

    pgsql_ip = "127.0.0.1"
    pgsql_port = 5432
    pgsql_db = "hasura"
    pgsql_user_name = "postgres"
    pgsql_user_pass = "root"

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
