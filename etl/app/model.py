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
    extra: dict[str, list] = None
    unique_id: str = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.url:
            self.unique_id = Utils.unique_hash(self.url)
