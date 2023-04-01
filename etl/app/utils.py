from __future__ import annotations

import datetime
import re
import time
import unittest
from hashlib import sha256
from typing import Any
from urllib.parse import urlparse

import dpath
import pytz

from settings import logger


class Utils:
    @classmethod
    def unique_hash(cls, *args) -> str:
        str_list = [str(item) for item in args]
        return sha256("".join(str_list).encode("utf-8")).hexdigest()

    @classmethod
    def json_path(cls, obj_dict: dict or list, string: str) -> Any:
        vals = dpath.values(obj_dict, string, separator=".")
        if len(vals) <= 0:
            return None
        elif len(vals) == 1:
            return vals[0]
        else:
            return vals

    @classmethod
    def get_name_from_url(cls, url: str) -> str:
        parsed_url = urlparse(url)
        host_name = parsed_url.netloc
        name_arr = host_name.split(".")
        if len(name_arr) <= 1:
            return name_arr[0]
        return name_arr[len(name_arr) - 2].capitalize()

    @classmethod
    def to_timestamp(cls, ts: int) -> int:
        if ts > (int(time.time()) * 10):
            return int(ts / 1000)
        return ts

    @classmethod
    def is_iso_datetime(cls, dt: str) -> bool:
        # 2021-08-11T10:30:00
        # 2021-08-11 10:30:00
        iso_pattern = r"^(?!.*Z)\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}$"
        return re.match(iso_pattern, dt) is not None

    @classmethod
    def is_utc_datetime(cls, dt: str) -> bool:
        utc_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
        return re.match(utc_pattern, dt) is not None

    @classmethod
    def to_utc_datetime(cls, dt: int | str) -> datetime:
        if isinstance(dt, int):
            dt = datetime.datetime.fromtimestamp(cls.to_timestamp(dt)).astimezone(
                pytz.UTC
            )
        elif isinstance(dt, str):
            dt = dt.strip()
            if cls.is_iso_datetime(dt):
                dt = datetime.datetime.fromisoformat(dt).astimezone(pytz.UTC)
            elif cls.is_utc_datetime(dt):
                dt = datetime.datetime.fromisoformat(dt.replace("Z", "")).astimezone(
                    pytz.UTC
                )
        return dt


class UtilsTestCase(unittest.TestCase):
    def test_unique_hash(self):
        self.assertEqual(
            Utils.unique_hash("1"),
            "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
        )
        self.assertEqual(
            Utils.unique_hash({"a": "1"}),
            "097553e04c9ead4a76b95db09d981efe4111f95990c41686c1c0f87625dbe96d",
        )
        self.assertNotEqual(Utils.unique_hash(["1"]), Utils.unique_hash("1"))
        self.assertEqual(Utils.unique_hash(1), Utils.unique_hash("1"))
        url = "https://forum.bnbchain.org/t/perplay-the-gaming-platfrom-that-lets-you-earn-while-you-play/843"
        self.assertEqual(
            Utils.unique_hash(url),
            "9c949a015983d1dcd6e3336008012563c918d7f9c343d8a50a65b38308f2b7dc",
        )
        url = "https://forum.bnbchain.org/t/bep-172-draft-improvement-on-bsc-validator-committing-stability"
        url_hash = "916a875a3f6a05a1ac6e01bca93c39777c8bf0bb261ba6085d9bc0e197774a45"
        self.assertEqual(Utils.unique_hash(url), url_hash)

    def test_dict_get(self):
        dict_or_list = [
            {
                "a": {"1": 0},
                "b": {"c": {"d": ["e", {"a": 1, "b": {"c": {"d": ["e", "f"]}}}]}},
            },
            {"tags": [{"alias": "a", "name": "1"}, {"alias": "b", "name": 2}]},
        ]

        self.assertEqual(
            Utils.json_path(dict_or_list, "0.b.c"),
            {"d": ["e", {"a": 1, "b": {"c": {"d": ["e", "f"]}}}]},
        )
        self.assertEqual(
            Utils.json_path(dict_or_list, "0.b.c.d.1.b.c"), {"d": ["e", "f"]}
        )

        # get value by array index
        self.assertEqual(Utils.json_path(dict_or_list, "0.b.c.d.0"), "e")
        self.assertEqual(
            Utils.json_path(dict_or_list, "0.b.c.d.1"),
            {"a": 1, "b": {"c": {"d": ["e", "f"]}}},
        )
        self.assertEqual(Utils.json_path(dict_or_list, "0.a.1"), 0)
        # key not exist
        self.assertEqual(Utils.json_path(dict_or_list, "0.e"), None)
        # array index too big
        self.assertEqual(Utils.json_path(dict_or_list, "2"), None)

        self.assertEqual(Utils.json_path(dict_or_list, "1.tags.*.name"), ["1", 2])

    def test_get_name_from_url(self):
        forum_urls = [
            "https://bnbchain.org",
            "https://ethereum-magicians.org",
            "https://forum.cosmos.network",
            "https://forum.polkadot.network",
            "https://gov.near.org",
            "https://forum.aptoslabs.com",
            "https://forum.astar.network",
            "https://forum.avax.network",
            "https://research.arbitrum.io",
            "https://forum.polygon.technology",
            "https://gov.optimism.io",
            "https://forums.sui.io",
            "https://forum.dfinity.org",
        ]
        for item in forum_urls:
            print(Utils.get_name_from_url(item))

    def test_to_timestamp(self):
        self.assertEqual(Utils.to_timestamp(1679734466000), 1679734466)
        self.assertEqual(Utils.to_timestamp(167973446600), 167973446)
        self.assertEqual(Utils.to_timestamp(16797344660), 16797344660)

    def test_to_utc_datetime(self):
        logger.debug(f"datatime: {Utils.to_utc_datetime(1679734466000)}")
        self.assertEqual(
            Utils.to_utc_datetime(1679734466000),
            datetime.datetime.fromisoformat("2023-03-25 08:54:26+00:00"),
        )
        self.assertEqual(
            Utils.to_utc_datetime(167973446600),
            datetime.datetime.fromisoformat("1975-04-29 03:17:26+00:00"),
        )
        # 2023-03-15T07:28:51Z
        # todo fix datetime error
        self.assertEqual(
            Utils.to_utc_datetime("2021-08-11T10:30:00Z"),
            datetime.datetime.fromisoformat("2021-08-11T10:30:00").astimezone(pytz.UTC),
        )
        self.assertEqual(
            Utils.to_utc_datetime("2021-08-11T10:30:00"),
            datetime.datetime.fromisoformat("2021-08-11T10:30:00").astimezone(pytz.UTC),
        )
        self.assertEqual(
            Utils.to_utc_datetime("2023-03-30 09:45:49"),
            datetime.datetime.fromisoformat("2023-03-30 09:45:49").astimezone(pytz.UTC),
        )


if __name__ == "__main__":
    unittest.main()
