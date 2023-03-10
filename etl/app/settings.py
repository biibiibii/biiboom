from pydantic import BaseSettings

from app.model import RequestNode, ResponseType, MatchRule


class Settings(BaseSettings):
    mongodb_database = "news_spider"
    mongodb_host = "127.0.0.1"
    mongodb_port = 27017
    mongodb_username = ""
    mongodb_password = ""

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
