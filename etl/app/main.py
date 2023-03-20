from app.model import Site, RequestSite
from app.rules import forum_rule
from app.settings import settings
from app.spiders.forum_spider import ForumSpider
from app.utils import Utils


def make_forum_requests(url_list: list) -> list[RequestSite]:
    rule = forum_rule
    sites = [
        Site(
            url=f"{item}/latest.json?no_definitions=true&page=0",
            jump_base_url=f"{item}/t/",
            rule_id=rule.id,
            name=Utils.get_name_from_url(item),
            sub_name="Forum",
        )
        for item in url_list
    ]

    return [RequestSite(site=site, rule=rule) for site in sites]


ForumSpider(request_sites=make_forum_requests(settings.forum_urls)).start()
