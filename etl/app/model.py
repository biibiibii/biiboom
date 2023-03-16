import datetime
import unittest
from enum import Enum
from typing import Any

from feapder import Item
from pydantic import BaseModel, PrivateAttr

from app.utils import Utils


class ResponseType(Enum):
    json = "json"
    html = "html"


class MatchRule(BaseModel):
    container: str
    title: str
    url: str
    desc: str = None
    created_at: str = None
    extra: dict[str, str] = None

    @property
    def unique_id(self) -> str:
        return Utils.unique_hash(self.unique_id)


class UrlNode(BaseModel):
    url: str
    jump_base_url: str = None


class RequestNode(BaseModel):
    url: str
    jump_base_url: str = None
    response_type: ResponseType
    rule: MatchRule

    _unique_id = PrivateAttr()

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._unique_id = Utils.unique_hash(self.url)

    @property
    def unique_id(self) -> str:
        return self._unique_id

    @classmethod
    def from_dict(cls, url_list: list[UrlNode], rule_dict: dict) -> "list[RequestNode]":
        return [__class__(**{**item.dict(), **rule_dict}) for item in url_list]


class Node(Item):
    url: str
    title: str
    desc: str = None
    parent_node: str
    extra: dict[str, list] = None
    unique_id: str = None
    created_at: datetime = None
    _last_updated_time: datetime = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.url:
            self.unique_id = Utils.unique_hash(self.url)
        self._last_updated_time = datetime.datetime.utcnow()

    @property
    def fingerprint(self):
        return self.unique_id


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
            response_type=ResponseType.json,
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
        print(RequestNode.from_dict([forum_request], forum_rule))


if __name__ == "__main__":
    unittest.main()
