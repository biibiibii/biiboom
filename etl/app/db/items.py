import datetime
import time
import unittest
from enum import Enum
from typing import Any

from feapder import Item, UpdateItem
from playhouse.shortcuts import model_to_dict
from pydantic import BaseModel

from db.model import SiteModel, SiteStatusEnum
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

    # todo create or update

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
    CEX = "cex"
    BLOG = "blog"
    FORUM = "forum"


class Site(UpdateItem):
    __update_key__ = ["next_update_time", "request_error_count"]
    id: str
    url: str
    jump_base_url: str = ""
    rule_id: str
    language: str
    name: str
    sub_name: str
    tags: list[str]
    update_rate: int
    next_update_time: int
    original_url: str
    status: str = SiteStatusEnum.ABLE.value

    request_method: str = "get"
    request_data: dict = None
    request_error_count: int = 0

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

    def request_callback(self, exception=False) -> None:
        """
        Crawl site fallback.
        :param exception:
        :return: None
        """
        if exception:
            self.request_error_count = self.request_error_count + 1
            self.next_update_time = int(time.time()) + (
                int(self.update_rate / 10) * self.request_error_count
            )
        else:
            self.request_error_count = 0
            self.next_update_time = int(time.time()) + self.update_rate

    def pre_to_db(self):
        pass

    @classmethod
    def get_or_create(cls, **kwargs) -> "Site":
        if "url" not in kwargs:
            raise Exception("url is None")
        site_id = Utils.unique_hash(kwargs["url"])
        site_model = SiteModel.get_or_none(SiteModel.id == site_id)
        if not site_model:
            logger.debug(f"site is None: {site_model}")
            return cls(**kwargs)
        else:
            model_dict = model_to_dict(
                site_model, recurse=False, extra_attrs=["rule_id"]
            )
            # todo update
            if "rule" in model_dict:
                del model_dict["rule"]

            return cls(**model_dict)


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
        self.posted_at = Utils.to_utc_datetime(self.posted_at)

        logger.debug(f"pre to db: {self.to_dict}")


class NodeTestCase(unittest.TestCase):
    def test_datetime(self):
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print(datetime.datetime.utcnow())

    def test_request_node(self):
        print(int(time.time()))
        pass

    def test_model_get(self):
        site_id = "bb246159cfc93001c0563ee62fd880d072e8a560c84585f1c60262d744aaeba5"
        # site_id = "bb246159cfc93001c0563ee62fd880d072e8a560c84585f1c60262d744aaeba"
        resp = SiteModel.get_or_none(SiteModel.id == site_id)
        logger.debug(f"resp: {resp}")


if __name__ == "__main__":
    unittest.main()
