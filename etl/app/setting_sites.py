"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-03
"""
import unittest

from app.db.db_client import db_client
from app.model import RequestSite, Site
from app.setting_rules import setting_rules
from app.settings import settings, logger
from app.utils import Utils


def make_forum_requests() -> list[RequestSite]:
    url_list = settings.forum_urls
    rule = setting_rules.rule_forum
    sites = [
        Site(
            url=f"{item}/latest.json?no_definitions=true&page=0",
            jump_base_url=f"{item}/t/",
            original_url=f"{item}/latest/",
            rule_id=rule.id,
            language="en",
            name=Utils.get_name_from_url(item),
            sub_name="Forum",
            tags=["forum"],
            update_rate=settings.site_update_rate,
        )
        for item in url_list
    ]

    return [RequestSite(site=site, rule=rule) for site in sites]


def make_chainfeeds_request() -> list[RequestSite]:
    url_list = settings.news_cn_urls
    rule = setting_rules.rule_chainfeeds
    sites = [
        Site(
            url=f"https://api.chainfeeds.xyz/feed/list?page=1&page_size=20&group_alias=selected",
            jump_base_url=f"https://www.chainfeeds.xyz/feed/detail/",
            original_url=f"{item}/",
            rule_id=rule.id,
            language="zh",
            name=Utils.get_name_from_url(item),
            sub_name="发现",
            tags=["news"],
            update_rate=settings.site_update_rate,
        )
        for item in url_list
    ]
    return [RequestSite(site=site, rule=rule) for site in sites]


_request_list = [
    globals()[func]()
    for func in dir()
    if callable(eval(func)) and func.startswith("make_")
]


class SettingSites:
    @property
    def request_sites(self) -> list[RequestSite]:
        __site_list = []
        for item in _request_list:
            for i in item:
                __site_list.append(i)
        return __site_list

    def update_sites(self):
        sites = self.request_sites
        db_client.put_items(sites)
        db_client.save()


setting_sites = SettingSites()


class RequestsTestCase(unittest.TestCase):
    def test_merge_list(self):
        logger.debug(f"{setting_sites.request_sites}")
        setting_sites.update_sites()
        pass

    def test_chainfeeds(self):
        pass


if __name__ == "__main__":
    unittest.main()
