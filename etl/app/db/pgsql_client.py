"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-03
"""
import unittest

from feapder import setting
from feapder_pipelines.db.pgsqldb import PgsqlDB

from settings_spider import settings_spider


class PgSqlClient(PgsqlDB):
    def __init__(self) -> None:
        # Init feapder setting
        for key, value in settings_spider.feapder_settings.items():
            setattr(setting, key, value)
        super().__init__()


if __name__ == "__main__":
    unittest.main()
