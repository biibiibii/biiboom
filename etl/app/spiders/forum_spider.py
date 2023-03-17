import unittest
from typing import Any

import feapder

from app.model import Site, RuleType, MatchRule, Node
from app.settings import settings, logger
from app.utils import Utils


def parse_html(request, response) -> list[Any]:
    logger.debug(f"parse_html")
    logger.debug(f"request param: {request.node}")
    rule = request.node.rule
    tds = response.xpath(rule.container)
    logger.debug(len(tds))
    nodes = []
    for td in tds:
        node = Node(
            title=td.xpath(rule.title).extract_first(),
            url=td.xpath(rule.url).extract_first(),
            site_id=request.node.id,
        )
        if rule.desc:
            node.desc = td.xpath(rule.desc).extract_first()
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
    logger.debug(f"parse json: {response.json}")
    nodes = []
    rule = request.node.rule
    data_list = Utils.json_path(response.json, rule.container)
    for item in data_list:
        item_url = Utils.json_path(item, rule.url)
        node = Node(
            title=Utils.json_path(item, rule.title),
            url=f"{request.node.jump_base_url}{item_url}"
            if request.node.jump_base_url
            else item_url,
            site_id=request.node.id,
        )
        if rule.desc:
            node.desc = Utils.json_path(item, rule.desc)
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

    def __init__(self, request_nodes: list[Site], thread_count=None):
        logger.info(f"start {self.__class__.__name__}...")
        super().__init__(thread_count)
        self.request_nodes = request_nodes

    def start_requests(self):
        for item in self.request_nodes:
            logger.info(f"start request url: {item.url}")
            yield feapder.Request(item.url, site=item)

    def parse(self, request, response):
        logger.debug(f"response type: {request.site.response_type}")
        if request.site.response_type == RuleType.html:
            nodes = parse_html(request, response)
        elif request.site.response_type == RuleType.json:
            nodes = parse_json(request, response)
        else:
            raise NotImplementedError("only support html/json")
        for item in nodes:
            yield item


class ForumSpiderTestCase(unittest.TestCase):
    def test_html(self):
        html_node = Site(
            url="https://forum.bnbchain.org/",
            response_type=RuleType.html,
            rule=MatchRule(
                container='.//td[@class="main-link"]',
                title='.//a[contains(@class,"title raw-link raw-topic-link")]/text()',
                url='.//a[contains(@class,"title raw-link raw-topic-link")]/@href',
                extra={
                    "category": './/span[@class="category-name"]/text()',
                    "tags": './/a[contains(@class,"discourse-tag")]/text()',
                },
            ),
        )

        ForumSpider(request_nodes=[html_node]).start()

    def test_json(self):
        url = "https://forum.aptoslabs.com"
        url = "https://forum.bnbchain.org"
        # url = "https://forum.astar.network"
        json_node = Site(
            url=f"{url}/latest.json?no_definitions=true&page=0",
            jump_base_url=f"{url}/t/",
            response_type=RuleType.json,
            rule=MatchRule(
                container="topic_list.topics",
                title="title",
                url="slug",
                created_at="created_at",
                extra={
                    "tags": "tags",
                },
            ),
        )
        ForumSpider(request_nodes=[json_node]).start()


if __name__ == "__main__":
    unittest.main()
