from app.model import UrlNode, RequestNode
from app.rules import forum_rule
from app.settings import settings
from app.spiders.forum_spider import ForumSpider


def make_forum_request(url_list: list) -> list[RequestNode]:
    url_nodes = [
        UrlNode(
            url=f"{item}/latest.json?&page=0",
            jump_base_url=f"{item}/t/",
        )
        for item in url_list
    ]
    return RequestNode.from_dict(url_nodes, forum_rule)


ForumSpider(request_nodes=make_forum_request(settings.forum_urls)).start()
