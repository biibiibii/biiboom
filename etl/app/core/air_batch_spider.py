"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-04
"""
import unittest

import feapder
from feapder import Item
from feapder.utils.log import log


class AirBatchSpider(feapder.AirSpider):
    def put_item(self, item: Item) -> None:
        log.debug(f"put_item: {item}")
        self._item_buffer.put_item(item)

    def pust_items(self, items: list[Item]) -> None:
        for item in items:
            self.put_item(item)


if __name__ == "__main__":
    unittest.main()
