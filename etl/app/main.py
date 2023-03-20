from app.db.db_client import db_client
from app.model import Site, RequestSite
from app.rules import rule_forum, rule_chainfeeds
from app.settings import settings
from app.spiders.forum_spider import ForumSpider
from app.utils import Utils


def make_forum_requests(url_list: list) -> list[RequestSite]:
    rule = rule_forum
    sites = [
        Site(
            url=f"{item}/latest.json?no_definitions=true&page=0",
            jump_base_url=f"{item}/t/",
            rule_id=rule.id,
            language="en",
            name=Utils.get_name_from_url(item),
            sub_name="Forum",
            tags=["forum"],
            update_rate=settings.site_update_rate,
        )
        for item in url_list
    ]
    db_client.put_items(sites)
    db_client.save()

    return [RequestSite(site=site, rule=rule) for site in sites]


def make_chainfeeds_request(url_list: list) -> list[RequestSite]:
    rule = rule_chainfeeds
    sites = [
        Site(
            url=f"https://api.chainfeeds.xyz/feed/list?page=1&page_size=20&group_alias=selected",
            jump_base_url=f"https://www.chainfeeds.xyz/feed/detail/",
            rule_id=rule.id,
            language="zh",
            name=Utils.get_name_from_url(item),
            sub_name="发现",
            tags=["news"],
            update_rate=settings.site_update_rate,
        )
        for item in url_list
    ]
    db_client.put_items(sites)
    db_client.save()
    return [RequestSite(site=site, rule=rule) for site in sites]


# ForumSpider(request_sites=make_forum_requests(settings.forum_urls)).start()
ForumSpider(request_sites=make_chainfeeds_request(settings.news_cn_urls)).start()
