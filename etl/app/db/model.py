"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-03
"""
import time
import unittest

from peewee import Model, CharField, IntegerField, ForeignKeyField
from playhouse.postgres_ext import PostgresqlExtDatabase, JSONField
from playhouse.shortcuts import model_to_dict

from settings import settings, logger

pgsql_db = PostgresqlExtDatabase(
    settings.pgsql_db,
    user=settings.pgsql_user_name,
    password=settings.pgsql_user_pass,
    host=settings.pgsql_ip,
    port=settings.pgsql_port,
)


class BaseExtModel(Model):
    class Meta:
        database = pgsql_db


class MatchRuleModel(BaseExtModel):
    id: str = CharField()
    container: str = CharField()
    title: str = CharField()
    url: str = CharField()
    posted_at: str = CharField()
    desc: str = CharField()
    extra: dict[str, str] = JSONField()
    note: str = CharField()
    rule_type: str = CharField()

    class Meta:
        database = pgsql_db
        table_name = "match_rule"


class SiteModel(BaseExtModel):
    id: str = CharField()
    url: str = CharField()
    jump_base_url: str = CharField()
    language: str = CharField()
    rule_id: str = CharField()
    name: str = CharField()
    sub_name: str = CharField()
    next_update_time: int = IntegerField()
    tags: list[str] = JSONField()
    update_rate: int = IntegerField()
    original_url: str = CharField()

    rule: MatchRuleModel = ForeignKeyField(MatchRuleModel)

    class Meta:
        database = pgsql_db
        table_name = "site"

    @classmethod
    def select_next_updates(cls) -> list["SiteModel"]:
        return (
            cls.select()
            .join(MatchRuleModel, on=(cls.rule_id == MatchRuleModel.id))
            .where(cls.next_update_time <= int(time.time()))
            .limit(settings.page_size)
        )


class SiteModelTestCase(unittest.TestCase):
    def test_select_next_updates(self):
        data_list = SiteModel.select_next_updates()
        logger.debug(f"data size: {len(data_list)}")
        for item in data_list:
            logger.debug(
                f"item: {item} {item.name} {item.rule_id} {item.rule.container}"
            )
            logger.debug(f"dict: {model_to_dict(item, backrefs=True)}")


if __name__ == "__main__":
    unittest.main()
