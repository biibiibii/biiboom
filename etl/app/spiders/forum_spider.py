import unittest
from typing import Any

import feapder

from core.air_batch_spider import AirBatchSpider
from db.items import Site, RuleType, Node, RequestSite, SiteLanguageEnum, SiteTagsEnum
from setting_rules import setting_rules
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
        if node.title and node.url and len(node.title) > 0 and len(node.url) > 0:
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
        if node.title and node.url and len(node.title) > 0 and len(node.url) > 0:
            nodes.append(node)
    logger.info(f"node size: {len(nodes)}")
    return nodes


class ForumSpider(AirBatchSpider):
    __custom_setting__ = settings_spider.feapder_settings
    logger.info(__custom_setting__)

    def __init__(self, request_sites: list[RequestSite], thread_count=None):
        logger.info(f"start {self.__class__.__name__}...")
        super().__init__(thread_count)
        self.request_nodes = request_sites

    def start_requests(self):
        for item in self.request_nodes:
            logger.info(f"start request url: {item.site.url}")
            # todo add request headers
            yield feapder.Request(
                item.site.url,
                method=item.site.request_method,
                # data=item.site.request_data,
                json=item.site.request_data,
                request_site=item,
            )

    def parse(self, request, response):
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
        site.request_callback()
        yield site

    def failed_request(self, request, response, e):
        self._failed_callback(request, response, e)

    def _failed_callback(self, request, response, e):
        logger.warning(f"_failed_callback: {e}")
        site = request.request_site.site
        site.request_callback(exception=True)
        self.put_item(site)


class ForumSpiderTestCase(unittest.TestCase):
    def test_json(self):
        rule = setting_rules.rule_cex_mexc_announcements

        section_id = "360000547811"
        original_url = f"https://www.mexc.com/support/sections/{section_id}"
        site = Site.get_or_create(
            url=f"https://www.mexc.com/help/announce/api/en-001/sections/{section_id}/articles?page=1&per_page=30",
            jump_base_url="https://www.mexc.com/support/articles/",
            original_url=original_url,
            rule_id=rule.id,
            language=SiteLanguageEnum.EN.value,
            name="Mexc",
            sub_name="Token Listing",
            tags=[SiteTagsEnum.CEX.value],
        )
        logger.debug(f"site: {site}")
        # item_client.save_item(site)
        sites = [RequestSite(site=site, rule=rule)]
        ForumSpider(request_sites=sites).start()

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
