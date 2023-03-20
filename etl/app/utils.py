import unittest
from hashlib import sha256
from typing import Any
from urllib.parse import urlparse


class Utils:
    @classmethod
    def unique_hash(cls, *args) -> str:
        str_list = [str(item) for item in args]
        return sha256("".join(str_list).encode("utf-8")).hexdigest()

    @classmethod
    def json_path(cls, obj_dict: dict or list, string: str) -> Any:
        if not string:
            return None
        k = string.split(".")
        for item in k:
            if item.isdigit() and isinstance(obj_dict, list):
                item = int(item)
            if item in obj_dict:
                obj_dict = obj_dict[item]
            elif isinstance(obj_dict, list) and item < len(obj_dict):
                obj_dict = obj_dict[item]
            else:
                return None
        return obj_dict

    @classmethod
    def get_name_from_url(cls, url: str) -> str:
        parsed_url = urlparse(url)
        host_name = parsed_url.netloc
        print(host_name.split("."))
        name_arr = host_name.split(".")
        if len(name_arr) <= 1:
            return name_arr[0]
        return name_arr[len(name_arr) - 2].capitalize()


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
            }
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
        self.assertEqual(Utils.json_path(dict_or_list, "1"), None)

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


if __name__ == "__main__":
    unittest.main()
