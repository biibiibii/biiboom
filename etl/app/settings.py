from pydantic import BaseSettings

from app.log_handler import LogHandler
from app.model import RequestNode, ResponseType, MatchRule


class Settings(BaseSettings):
    log_name = "etl"
    log_level = "DEBUG"
    mongodb_database = "news_spider"
    mongodb_host = "127.0.0.1"
    mongodb_port = 27017
    mongodb_username = "root"
    mongodb_password = "root"
    redisdb_ip_ports = "127.0.0.1:6379"
    redisdb_user_pass = ""

    hello_node = RequestNode(
        url="https://ethereum-magicians.org/",
        response_type=ResponseType.html,
        rule=MatchRule(
            container='.//td[@class="main-link"]',
            title='.//a[contains(@class,"title raw-link raw-topic-link")]/text()',
            url='.//a[contains(@class,"title raw-link raw-topic-link")]/@href',
        ),
    )


settings = Settings()
logger = LogHandler(settings.log_name, settings.log_level)
