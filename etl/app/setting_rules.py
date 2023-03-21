import unittest

from pydantic import BaseSettings

from app.db.db_client import db_client
from app.model import RuleType, MatchRule
from app.settings import logger

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
    rule_chainfeeds = MatchRule(
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

    def update_rules(self):
        _rules = [self.dict().get(item) for item in self.dict()]
        logger.debug(f"all rules: {_rules}")
        db_client.put_items(_rules)
        db_client.save()


setting_rules = SettingRules()


class RequestsTestCase(unittest.TestCase):
    @staticmethod
    def test_rule_settings():
        logger.debug(f"rule settings: {setting_rules}")

    @staticmethod
    def test_update_rules():
        setting_rules.update_rules()
        pass


if __name__ == "__main__":
    unittest.main()
