import feapder
from feapder.utils.log import log

from app.model import RequestNode, ResponseType, MatchRule, Node
from app.settings import settings


class ForumSpider(feapder.AirSpider):
    __custom_setting__ = dict(
        # ITEM_PIPELINES=["feapder.pipelines.mongo_pipeline.MongoPipeline"],
        SPIDER_MAX_RETRY_TIMES=1,
        MONGO_IP=settings.mongodb_host,
        MONGO_PORT=settings.mongodb_port,
        MONGO_DB=settings.mongodb_database,
        MONGO_USER_NAME=settings.mongodb_username,
        MONGO_USER_PASS=settings.mongodb_password,
        LOG_LEVEL="DEBUG",
    )

    def __init__(self, request_nodes: list[RequestNode], thread_count=None):
        super().__init__(thread_count)
        self.request_nodes = request_nodes

    def start_requests(self):
        for item in self.request_nodes:
            yield feapder.Request(item.url, node=item)

    def parse(self, request, response):
        log.debug(f"request param: {request.node}")
        rule = request.node.rule
        tds = response.xpath(rule.container)
        log.debug(len(tds))
        nodes = []
        for td in tds:
            node = Node(
                title=td.xpath(rule.title).extract_first(),
                url=td.xpath(rule.url).extract_first(),
            )
            if rule.desc:
                node.desc = td.xpath(rule.desc).extract_first()
            if rule.extra:
                extra = dict()
                for item in rule.extra:
                    extra[item] = td.xpath(rule.extra[item]).extract()
                node.extra = extra
            nodes.append(node)
            log.debug(f"node: {node}")
        log.info(f"node size: {len(nodes)}")


if __name__ == "__main__":
    url = "https://ethereum-magicians.org/"
    url = "https://forum.bnbchain.org/"

    hello_node = RequestNode(
        url=url,
        response_type=ResponseType.html,
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
    ForumSpider([hello_node]).start()
