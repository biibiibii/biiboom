import unittest
from hashlib import sha256


class Utils:
    @classmethod
    def unique_hash(cls, *args) -> str:
        str_list = [str(item) for item in args]
        return sha256("".join(str_list).encode("utf-8")).hexdigest()


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


if __name__ == "__main__":
    unittest.main()
