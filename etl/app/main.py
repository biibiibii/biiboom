from app.model import UrlNode, Site
from app.rules import forum_rule
from app.settings import settings
from app.spiders.forum_spider import ForumSpider


def make_forum_request(url_list: list) -> list[Site]:
    url_nodes = [
        UrlNode(
            url=f"{item}/latest.json?&page=0",
            jump_base_url=f"{item}/t/",
        )
        for item in url_list
    ]
    return Site.from_dict(url_nodes, forum_rule)


ForumSpider(request_sites=make_forum_request(settings.forum_urls)).start()
