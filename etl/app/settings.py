import os

from pydantic import BaseSettings

from log_handler import LogHandler

logger = LogHandler("settings", "INFO")


class Settings(BaseSettings):
    log_name = "etl"
    log_level = "DEBUG"

    pgsql_ip = "127.0.0.1"
    pgsql_port = 5432
    pgsql_db = "hasura"
    pgsql_user_name = "postgres"
    pgsql_user_pass = "root"

    spider_thread_count = 3

    site_update_rate = 3600

    page_size = 50

    # schedule job time: second
    scheduler_trigger = 120

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

    news_cn_urls = ["https://www.chainfeeds.xyz"]

    class Config:
        env_file = "./app/.local.env"
        env_file_encoding = "utf-8"


env_list = {
    "local": "./app/.local.env",
    "dev": "./app/.dev.env",
    "prod": "./app/.prod.env",
}
env = os.getenv("env", "local")
logger.info("env: {} ---> load env file: {}".format(env, env_list[env]))

if env not in env_list.keys():
    raise Exception("env: {} not supported. support env: ".format(env, env_list))

settings = Settings(_env_file=env_list[env], _env_file_encoding="utf-8")
logger = LogHandler(settings.log_name, settings.log_level)
logger.debug(settings.dict())
