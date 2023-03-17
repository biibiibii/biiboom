import datetime
import unittest
from enum import Enum
from typing import Any

from feapder import Item
from pydantic import BaseModel

from app.utils import Utils


class RuleType(Enum):
    json = "json"
    html = "html"


class MatchRule(Item):
    id: str
    container: str
    title: str
    url: str
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


class Site(Item):
    id: str
    url: str
    jump_base_url: str = None
    rule_id: str

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.id = Utils.unique_hash(self.url)

    @property
    def fingerprint(self):
        return self.id

    @classmethod
    def from_dict(cls, url_list: list[UrlNode], rule_dict: dict) -> "list[Site]":
        return [__class__(**{**item.dict(), **rule_dict}) for item in url_list]


class Node(Item):
    id: str
    site_id: str
    url: str
    title: str
    desc: str = None
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
        forum_request = UrlNode(
            url="https://forum.bnbchain.org/latest.json?&page=0",
            jump_base_url="https://forum.bnbchain.org/t/",
        )
        forum_rule = dict(
            response_type=RuleType.json,
            rule=MatchRule(
                container="//topic_list/topics",
                title="title/text()",
                url="slug/text()",
                created_at="created_at/text()",
                extra={
                    "tags": "tags/item/text()",
                },
            ),
        )
        print(Site.from_dict([forum_request], forum_rule))


if __name__ == "__main__":
    unittest.main()
