"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-03
"""
import unittest

from playhouse.shortcuts import model_to_dict
from pydantic import BaseSettings

from db.item_client import item_client
from db.items import RequestSite, Site, MatchRule
from db.model import SiteModel
from setting_rules import setting_rules
from settings import settings, logger
from spiders.forum_spider import ForumSpider
from utils import Utils

__all__ = ["setting_sites"]


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
        )
        for item in url_list
    ]
    return [RequestSite(site=site, rule=rule) for site in sites]


def make_marbits_request() -> list[RequestSite]:
    rule = setting_rules.rule_marsbit
    original_url = "https://www.marsbit.co/"
    site = Site(
        url=f"https://api.marsbit.co/info/news/shownews",
        jump_base_url="https://news.marsbit.co/{id}.html",
        original_url=original_url,
        rule_id=rule.id,
        language="zh",
        name=Utils.get_name_from_url(original_url),
        sub_name="新闻",
        tags=["news"],
    )
    return [RequestSite(site=site, rule=rule)]


def make_bnbchain_blog_request() -> list[RequestSite]:
    rule = setting_rules.rule_bnbchain_blog
    original_url = "https://bnbchain.org/en/blog/"
    site = Site(
        url=f"https://bnbchain.org/en/blog/page-data/index/page-data.json",
        jump_base_url="https://bnbchain.org/en/blog/",
        original_url=original_url,
        rule_id=rule.id,
        language="en",
        name=Utils.get_name_from_url(original_url),
        sub_name="blog",
        tags=["blog"],
    )
    return [RequestSite(site=site, rule=rule)]


def make_ethereum_blog_request() -> list[RequestSite]:
    rule = setting_rules.rule_ethereum_blog
    original_url = "https://blog.ethereum.org/"
    site = Site(
        url=f"https://blog.ethereum.org/_next/data/4tYBiKFBGW9-G-BSIr4zA/en.json",
        jump_base_url=original_url,
        original_url=original_url,
        rule_id=rule.id,
        language="en",
        sub_name="blog",
        tags=["blog"],
    )
    return [RequestSite(site=site, rule=rule)]


_request_list = [
    globals()[func]()
    for func in dir()
    if callable(eval(func)) and func.startswith("make_")
]


class SettingSites(BaseSettings):
    @property
    def request_sites(self) -> list[RequestSite]:
        __site_list = []
        for item in _request_list:
            for i in item:
                __site_list.append(i)
        return __site_list

    def update_sites(self):
        sites = self.request_sites
        for site in sites:
            item_client.put_item(site.site)
            item_client.put_item(site.rule)
        item_client.save()

    @classmethod
    def get_next_updates(cls) -> list[RequestSite]:
        update_sites = SiteModel.select_next_updates()
        __site_list = []
        for item in update_sites:
            item.rule_id = item.rule.id
            item_dict = model_to_dict(item, backrefs=False)
            if "rule" in item_dict:
                del item_dict["rule"]
            item_dict["rule_id"] = item.rule_id
            __site_list.append(
                RequestSite(
                    site=Site(**item_dict),
                    rule=MatchRule(**model_to_dict(item.rule)),
                )
            )

        return __site_list


setting_sites = SettingSites()


class RequestsTestCase(unittest.TestCase):
    def test_update_sites(self):
        setting_sites.update_sites()

    def test_merge_list(self):
        logger.debug(f"{setting_sites.request_sites}")
        setting_sites.update_sites()
        pass

    def test_get_next_updates(self):
        next_updates = setting_sites.get_next_updates()
        logger.debug(f"updates: {next_updates}")

    def test_chainfeeds(self):
        feeds = make_chainfeeds_request()
        ForumSpider(request_sites=feeds).start()
        pass

    def test_marsbit(self):
        marsbit = make_marbits_request()
        ForumSpider(request_sites=marsbit).start()

    def test_bnbchain_blog(self):
        bnbchain_blog = make_bnbchain_blog_request()
        ForumSpider(request_sites=bnbchain_blog).start()

    def test_ethereum_blog(self):
        ethereum = make_ethereum_blog_request()
        ForumSpider(request_sites=ethereum).start()


if __name__ == "__main__":
    unittest.main()
