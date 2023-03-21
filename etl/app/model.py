import datetime
import time
import unittest
from enum import Enum
from typing import Any

from feapder import Item, UpdateItem
from pydantic import BaseModel

from app.settings import settings
from app.utils import Utils


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


class Site(UpdateItem):
    __update_key__ = ["next_update_time", "original_url"]
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

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.id = Utils.unique_hash(self.url)
        if "update_rate" not in self.to_dict:
            self.update_rate = settings.site_update_rate
        self.next_update_time = int(time.time()) + self.update_rate

    @property
    def fingerprint(self):
        return self.id

    @classmethod
    def from_dict(cls, url_list: list[UrlNode], rule_dict: dict) -> "list[Site]":
        return [__class__(**{**item.dict(), **rule_dict}) for item in url_list]


class RequestSite(BaseModel):
    site: Site
    rule: MatchRule

    class Config:
        arbitrary_types_allowed = True


class Node(Item):
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


class NodeTestCase(unittest.TestCase):
    def test_datetime(self):
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print(datetime.datetime.utcnow())

    def test_request_node(self):
        print(int(time.time()))
        pass


if __name__ == "__main__":
    unittest.main()
