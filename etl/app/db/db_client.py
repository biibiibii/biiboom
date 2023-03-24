"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-03
"""
import unittest

from feapder import Item, setting
from feapder.buffer.item_buffer import ItemBuffer

from settings import settings


class DbClient:
    def __init__(self) -> None:
        self._redis_key = "db_client"
        # Init feapder setting
        for key, value in settings.feapder_settings.items():
            setattr(setting, key, value)

        self._item_buffer = None

    def put_items(self, items: list[Item]):
        for item in items:
            self.put_item(item)

    def put_item(self, item: Item):
        if not self._item_buffer:
            self._item_buffer = ItemBuffer(redis_key=self._redis_key)
            self._item_buffer.start()
        self._item_buffer.put_item(item)

    def save(self):
        self._item_buffer.flush()
        self._item_buffer.stop()


db_client = DbClient()

if __name__ == "__main__":
    unittest.main()
