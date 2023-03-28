import unittest
from typing import Any

import feapder

from db.items import Site, RuleType, MatchRule, Node, RequestSite
from settings import logger
from settings_spider import settings_spider
from utils import Utils


def parse_html(request, response) -> list[Any]:
    rule = request.request_site.rule
    site = request.request_site.site
    logger.debug(f"parse_html: {site}")

    tds = response.xpath(rule.container)
    logger.debug(len(tds))
    nodes = []
    for td in tds:
        node = Node(
            title=td.xpath(rule.title).extract_first(),
            url=td.xpath(rule.url).extract_first(),
            site_id=site.id,
        )
        if rule.desc:
            node.desc = td.xpath(rule.desc).extract_first()
        if rule.posted_at:
            node.posted_at = td.xpath(rule.posted_at).extract_first()
        if rule.extra:
            extra = dict()
            for item in rule.extra:
                extra[item] = td.xpath(rule.extra[item]).extract()
            node.extra = extra
        if len(node.title) > 0 and len(node.url) > 0:
            nodes.append(node)
        logger.debug(f"node: {node}")
    logger.info(f"node size: {len(nodes)}")
    return nodes


def parse_jump_url(base_url: str, item_url_id: str) -> str:
    if not base_url:
        return item_url_id
    if "{id}" in base_url:
        return base_url.replace("{id}", item_url_id)
    return f"{base_url}{item_url_id}"


def parse_json(request, response):
    rule = request.request_site.rule
    site = request.request_site.site
    logger.debug(f"parse json: {site}")
    nodes = []

    data_list = Utils.json_path(response.json, rule.container)
    for item in data_list:
        item_url_id = Utils.json_path(item, rule.url)
        node = Node(
            title=Utils.json_path(item, rule.title),
            url=parse_jump_url(site.jump_base_url, item_url_id),
            site_id=site.id,
        )
        if rule.desc:
            node.desc = Utils.json_path(item, rule.desc)
        if rule.posted_at:
            node.posted_at = Utils.json_path(item, rule.posted_at)
        if rule.extra:
            extra = dict()
            for i in rule.extra:
                extra[i] = Utils.json_path(item, rule.extra[i])
            node.extra = extra
        logger.debug(f"node: {node}")
        if len(node.title) > 0 and len(node.url) > 0:
            nodes.append(node)
    logger.info(f"node size: {len(nodes)}")
    return nodes


class ForumSpider(feapder.AirSpider):
    __custom_setting__ = settings_spider.feapder_settings
    logger.info(__custom_setting__)

    def __init__(self, request_sites: list[RequestSite], thread_count=None):
        logger.info(f"start {self.__class__.__name__}...")
        super().__init__(thread_count)
        self.request_nodes = request_sites

    def start_requests(self):
        for item in self.request_nodes:
            logger.info(f"start request url: {item.site.url}")
            yield feapder.Request(
                item.site.url,
                method=item.site.request_method,
                data=item.site.request_data,
                request_site=item,
            )

    def parse(self, request, response):
        logger.debug(f"response: {response.text}")
        rule = request.request_site.rule
        site = request.request_site.site

        logger.debug(f"parse rule: {rule}")
        if rule.rule_type == RuleType.html.value:
            nodes = parse_html(request, response)
        elif rule.rule_type == RuleType.json.value:
            nodes = parse_json(request, response)
        else:
            raise NotImplementedError("only support html/json")
        for item in nodes:
            yield item
        # Update next update time
        site.update_next_time()
        yield site
        # yield rule


class ForumSpiderTestCase(unittest.TestCase):
    def test_json(self):
        url = "https://forum.aptoslabs.com"
        url = "https://forum.bnbchain.org"
        # url = "https://forum.astar.network"
        rule_item = MatchRule(
            container="topic_list.topics",
            title="title",
            # url="slug",
            url="id",
            rule_type=RuleType.json.value,
            posted_at="created_at",
            extra={
                "tags": "tags",
            },
        )

        site = Site(
            url=f"{url}/latest.json?no_definitions=true&page=0",
            jump_base_url=f"{url}/t/",
            rule_id=rule_item.id,
        )

        request_site = RequestSite(site=site, rule=rule_item)
        logger.debug(f"site:{site}")

        ForumSpider(request_sites=[request_site]).start()

    def test_parse_jump_url(self):
        base_url = "https://news.marsbit.co/{id}.html"
        item_id = "20230325094746660158"
        self.assertEqual(
            parse_jump_url(base_url, item_id),
            "https://news.marsbit.co/20230325094746660158.html",
        )
        base_url = "https://www.chainfeeds.xyz/feed/detail/"
        item_id = "68c58246-44ea-47a0-8eea-8087fa9898ad"
        self.assertEqual(
            parse_jump_url(base_url, item_id),
            "https://www.chainfeeds.xyz/feed/detail/68c58246-44ea-47a0-8eea-8087fa9898ad",
        )


if __name__ == "__main__":
    unittest.main()
