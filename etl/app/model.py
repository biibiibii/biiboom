import datetime
import unittest
from enum import Enum

from feapder import Item
from pydantic import BaseModel

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


class RequestNode(BaseModel):
    url: str
    response_type: ResponseType
    rule: MatchRule

    @property
    def unique_id(self) -> str:
        return Utils.unique_hash(self.url)


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


if __name__ == "__main__":
    unittest.main()
