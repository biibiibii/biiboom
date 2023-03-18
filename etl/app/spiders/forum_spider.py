import unittest
from typing import Any

import feapder

from app.model import Site, RuleType, MatchRule, Node, RequestSite
from app.settings import settings, logger
from app.utils import Utils


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
        nodes.append(node)
        logger.debug(f"node: {node}")
    logger.info(f"node size: {len(nodes)}")
    return nodes


def parse_json(request, response):
    rule = request.request_site.rule
    site = request.request_site.site
    logger.debug(f"parse json: {site}")
    nodes = []

    data_list = Utils.json_path(response.json, rule.container)
    for item in data_list:
        item_url = Utils.json_path(item, rule.url)
        node = Node(
            title=Utils.json_path(item, rule.title),
            url=f"{site.jump_base_url}{item_url}" if site.jump_base_url else item_url,
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
        nodes.append(node)
    logger.info(f"node size: {len(nodes)}")
    return nodes


class ForumSpider(feapder.AirSpider):
    __custom_setting__ = dict(
        ITEM_PIPELINES=["feapder_pipelines.pipelines.pgsql_pipeline.PgsqlPipeline"],
        SPIDER_MAX_RETRY_TIMES=1,
        SPIDER_THREAD_COUNT=settings.max_thread_count,
        # MYSQL_IP=settings.mysql_ip,
        # MYSQL_PORT=settings.mysql_port,
        # MYSQL_DB=settings.mysql_db,
        # MYSQL_USER_NAME=settings.mysql_user_name,
        # MYSQL_USER_PASS=settings.mysql_user_pass,
        PGSQL_IP=settings.pgsql_ip,
        PGSQL_PORT=settings.pgsql_port,
        PGSQL_DB=settings.pgsql_db,
        PGSQL_USER_NAME=settings.pgsql_user_name,
        PGSQL_USER_PASS=settings.pgsql_user_pass,
        LOG_LEVEL="INFO",
    )

    def __init__(self, request_sites: list[RequestSite], thread_count=None):
        logger.info(f"start {self.__class__.__name__}...")
        super().__init__(thread_count)
        self.request_nodes = request_sites

    def start_requests(self):
        for item in self.request_nodes:
            logger.info(f"start request url: {item.site.url}")
            yield feapder.Request(item.site.url, request_site=item)

    def parse(self, request, response):
        rule = request.request_site.rule
        site = request.request_site.site

        logger.debug(f"response type: {rule}")
        if rule.rule_type == RuleType.html.value:
            nodes = parse_html(request, response)
        elif rule.rule_type == RuleType.json.value:
            nodes = parse_json(request, response)
        else:
            raise NotImplementedError("only support html/json")
        for item in nodes:
            yield item
        yield site
        yield rule


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
        rule_item.to_UpdateItem()
        site = Site(
            url=f"{url}/latest.json?no_definitions=true&page=0",
            jump_base_url=f"{url}/t/",
            rule_id=rule_item.id,
        )
        site.to_UpdateItem()
        request_site = RequestSite(site=site, rule=rule_item)

        ForumSpider(request_sites=[request_site]).start()


if __name__ == "__main__":
    unittest.main()
