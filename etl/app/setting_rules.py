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
            # todo support json array
            "tags": "tags.0.tag_name",
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

    def update_rules(self):
        _rules = [self.dict().get(item) for item in self.dict()]
        logger.debug(f"all rules: {_rules}")
        item_client.put_items(_rules)
        item_client.save()


setting_rules = SettingRules()


class RequestsTestCase(unittest.TestCase):
    def test_rule_settings(self):
        logger.debug(f"rule settings: {setting_rules}")

    def test_update_rules(self):
        setting_rules.update_rules()
        pass


if __name__ == "__main__":
    unittest.main()
