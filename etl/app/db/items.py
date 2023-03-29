import datetime
import time
import unittest
from enum import Enum
from typing import Any

import pytz
from feapder import Item, UpdateItem
from pydantic import BaseModel

from settings import settings, logger
from utils import Utils


class RuleType(Enum):
    json = "json"
    html = "html"


class MatchRule(Item):
    id: str
    container: str
    title: str
    url: str
    posted_at: str = None
    desc: str = None
    extra: dict[str, str] = None
    note: str = None
    rule_type: str = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = Utils.unique_hash(
            [
                self.container,
                self.title,
                self.url,
                self.desc,
                self.extra,
                self.rule_type,
            ]
        )

    @property
    def fingerprint(self):
        return self.id


class UrlNode(BaseModel):
    url: str
    jump_base_url: str = None


class SiteLanguageEnum(Enum):
    EN = "en"
    ZH = "zh"


class SiteTagsEnum(Enum):
    NEWS = "news"
    BLOG = "blog"
    FORUM = "forum"


class Site(UpdateItem):
    __update_key__ = ["next_update_time"]
    id: str
    url: str
    jump_base_url: str = None
    rule_id: str
    language: str
    name: str
    sub_name: str
    tags: list[str]
    update_rate: int
    next_update_time: int
    original_url: str

    request_method: str = "get"
    request_data: str = None

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.id = Utils.unique_hash(self.url)
        if "update_rate" not in self.to_dict:
            self.update_rate = settings.site_update_rate
        if "name" not in self.to_dict:
            self.name = Utils.get_name_from_url(self.original_url)

    @property
    def fingerprint(self):
        return self.id

    def update_next_time(self):
        self.next_update_time = int(time.time()) + self.update_rate


class RequestSite(BaseModel):
    site: Site
    rule: MatchRule

    class Config:
        arbitrary_types_allowed = True


class Node(UpdateItem):
    __update_key__ = ["posted_at", "url", "title", "extra"]
    id: str
    site_id: str
    url: str
    title: str
    desc: str = None
    posted_at: datetime = None
    extra: dict[str, list] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = Utils.unique_hash([self.site_id, self.url])

    @property
    def fingerprint(self):
        return self.id

    def pre_to_db(self):
        logger.debug(f"pre to db: {self.to_dict}")
        if isinstance(self.posted_at, int):
            self.posted_at = datetime.datetime.fromtimestamp(
                Utils.to_timestamp(self.posted_at)
            ).astimezone(pytz.UTC)
        logger.debug(f"pre to db: {self.to_dict}")


class NodeTestCase(unittest.TestCase):
    def test_datetime(self):
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print(datetime.datetime.utcnow())

    def test_request_node(self):
        print(int(time.time()))
        pass


if __name__ == "__main__":
    unittest.main()
