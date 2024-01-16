import unittest

from pydantic import BaseSettings

from db.item_client import item_client
from db.items import RuleType, MatchRule
from settings import logger

__all__ = ["setting_rules"]


class SettingRules(BaseSettings):
    # https://forum.bnbchain.org/ => https://forum.bnbchain.org/latest.json?&page=0
    # https://ethereum-magicians.org/ => https://ethereum-magicians.org/latest.json?no_definitions=true&page=0
    rule_forum = MatchRule(
        container="topic_list.topics",
        title="title",
        url="id",
        rule_type=RuleType.json.value,
        posted_at="created_at",
        extra={
            "tags": "tags",
        },
    )

    # https://www.chainfeeds.xyz/
    rule_news_chainfeeds = MatchRule(
        container="data.list",
        title="title",
        url="uuid",
        rule_type=RuleType.json.value,
        posted_at="show_time",
        extra={
            "tags": "tags.*.tag_name",
        },
    )

    # https://www.marsbit.co/
    # https://api.marsbit.co/info/news/showinfo
    rule_news_marsbit = MatchRule(
        container="obj.inforList",
        title="title",
        url="id",
        rule_type=RuleType.json.value,
        posted_at="createTime",
        extra={},
    )

    # https://www.odaily.news/
    # https://www.odaily.news/api/pp/api/app-front/feed-stream?feed_id=280&b_id=&per_page=50
    rule_news_odaily = MatchRule(
        container="data.items",
        title="title",
        url="entity_id",
        rule_type=RuleType.json.value,
        posted_at="published_at",
        extra={},
    )

    # https://www.wu-talk.com/
    # https://api.wu-talk.com/api/site/getAllArticleList
    rule_news_wutalk = MatchRule(
        container="data",
        title="title",
        url="url",
        rule_type=RuleType.json.value,
        posted_at="inputtime",
        extra={},
    )

    # https://www.panewslab.com/zh/index.html
    # https://www.panewslab.com/webapi/index/list?Rn=30&LId=1&LastTime=
    rule_news_panews = MatchRule(
        container="data",
        title="title",
        url="id",
        rule_type=RuleType.json.value,
        posted_at="publishTime",
        extra={"tags": "tags"},
    )

    # https://www.jinse.com/
    # https://api.jinse.cn/noah/v3/timelines?catelogue_key=www&limit=50&information_id=&flag=down
    rule_news_jinse = MatchRule(
        container="data.list",
        title="object_1.title",
        url="object_1.jump_url",
        rule_type=RuleType.json.value,
        posted_at="object_1.published_at",
        extra={},
    )

    rule_news_8btc = MatchRule(
        container="//ul[contains(@class,'bbt-list')]/li",
        title="./a/text()",
        url="./a/@href",
        rule_type=RuleType.html.value,
        posted_at="./a/span/text()",
        extra={},
    )

    rule_news_chaincatcher = MatchRule(
        container="data",
        title="title",
        url="id",
        rule_type=RuleType.json.value,
        posted_at="add_time",
        extra={},
    )
    # https://www.theblockbeats.info/article
    # https://api.theblockbeats.info/v3/Information/newsall?page=1
    rule_news_blockbeats = MatchRule(
        container="data",
        title="title",
        url="id",
        rule_type=RuleType.json.value,
        posted_at="add_time",
        extra={"tags": "topic_title"},
    )
    # https://www.theblockbeats.info/newsflash
    # https://api.theblockbeats.info/v3/newsflash/select?page=1
    rule_news_blockbeats_flash = MatchRule(
        container="data.data",
        title="title",
        url="id",
        rule_type=RuleType.json.value,
        posted_at="add_time",
        extra={},
    )

    rule_news_tokeninsight = MatchRule(
        container="data.list",
        title="title",
        url="articleLink",
        rule_type=RuleType.json.value,
        posted_at="onlineTime",
        extra={},
    )

    rule_cex_binance_news = MatchRule(
        container="data.catalogs.1.articles",
        title="title",
        url="code",
        rule_type=RuleType.json.value,
        posted_at="releaseDate",
        extra={},
    )

    rule_cex_binance_tokenlisting = MatchRule(
        container="data.catalogs.0.articles",
        title="title",
        url="code",
        rule_type=RuleType.json.value,
        posted_at="releaseDate",
        extra={},
    )

    # https://www.okx.com/help-center/section/latest-announcements
    rule_cex_okx_news = MatchRule(
        container="data.notices",
        title="title",
        url="shareLink",
        rule_type=RuleType.json.value,
        posted_at="publishDate",
        extra={},
    )

    # https://www.kucoin.com/_api/cms/articles?category=announcements&lang=en_US&page=1&pageSize=20
    rule_cex_kucoin_announcements = MatchRule(
        container="items",
        title="title",
        url="path",
        rule_type=RuleType.json.value,
        posted_at="publish_ts",
        extra={},
    )

    # https://www.mexc.com/help/announce/api/en-001/sections/360000679912/articles?page=1&per_page=30
    rule_cex_mexc_announcements = MatchRule(
        container="articles",
        title="title",
        url="id",
        rule_type=RuleType.json.value,
        posted_at="created_at",
        extra={},
    )

    # bnbchain blog
    # https://bnbchain.org/en/blog/page-data/index/page-data.json
    # https://bnbchain.org/en/blog/page-data/page/2/page-data.json
    rule_blog_bnbchain = MatchRule(
        container="result.data.en.edges",
        title="node.title",
        url="node.slug",
        rule_type=RuleType.json.value,
        posted_at="node.published_at",
        extra={},
    )
    # binance blog
    # https://www.binance.com/bapi/composite/v1/public/content/blog/list?category=&tag=&page=1&size=20
    rule_blog_binance = MatchRule(
        container="data.blogList",
        title="title",
        url="id",
        rule_type=RuleType.json.value,
        posted_at="postTime",
        extra={
            "tags": "tag.*.name",
        },
    )

    # https://blog.ethereum.org/
    # https://blog.ethereum.org/_next/data/4tYBiKFBGW9-G-BSIr4zA/en.json
    rule_blog_ethereum = MatchRule(
        container="pageProps.allPostsData",
        title="frontmatter.title",
        url="url",
        rule_type=RuleType.json.value,
        posted_at="frontmatter.date",
        extra={
            "tags": "frontmatter.category",
        },
    )

    # https://polkadot.network/blog/
    # https://polkadot.network/page-data/blog/page-data.json
    rule_blog_polkadot = MatchRule(
        container="result.data.posts.edges",
        title="node.title",
        url="node.slug",
        rule_type=RuleType.json.value,
        posted_at="node.published_at",
        extra={},
    )

    def update_rules(self):
        _rules = [self.dict().get(item) for item in self.dict()]
        logger.debug(f"all rules: {_rules}")
        item_client.put_items(_rules)
        item_client.save()

    def update_rule(self, rule: MatchRule):
        item_client.put_item(rule)
        item_client.save()


setting_rules = SettingRules()


class RequestsTestCase(unittest.TestCase):
    def test_rule_settings(self):
        logger.debug(f"rule settings: {setting_rules}")

    def test_update_rules(self):
        setting_rules.update_rules()

    def test_marbits_rule(self):
        rule = setting_rules.rule_news_marsbit
        logger.debug(f"rule: {rule}")
        self.assertEqual(
            rule.id, "ecca8b8e9e060bde8910fd12a05bb444a55f338788d68f2c8e00e1fb03070a54"
        )


if __name__ == "__main__":
    unittest.main()
