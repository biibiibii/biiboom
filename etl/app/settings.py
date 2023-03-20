from pydantic import BaseSettings

from app.log_handler import LogHandler


class Settings(BaseSettings):
    log_name = "etl"
    log_level = "DEBUG"

    pgsql_ip = "127.0.0.1"
    pgsql_port = 5432
    pgsql_db = "hasura"
    pgsql_user_name = "postgres"
    pgsql_user_pass = "root"

    redisdb_ip_ports = "127.0.0.1:6379"
    redisdb_user_pass = ""
    spider_thread_count = 3

    site_update_rate = 3600

    feapder_settings = dict(
        ITEM_PIPELINES=["feapder_pipelines.pipelines.pgsql_pipeline.PgsqlPipeline"],
        SPIDER_MAX_RETRY_TIMES=1,
        SPIDER_THREAD_COUNT=spider_thread_count,
        PGSQL_IP=pgsql_ip,
        PGSQL_PORT=pgsql_port,
        PGSQL_DB=pgsql_db,
        PGSQL_USER_NAME=pgsql_user_name,
        PGSQL_USER_PASS=pgsql_user_pass,
        LOG_LEVEL="INFO",
    )

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
        "https://forum.dfinity.org",
    ]


settings = Settings()
logger = LogHandler(settings.log_name, settings.log_level)
