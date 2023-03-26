"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-03
"""
import unittest

from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.blocking import BlockingScheduler

from setting_sites import setting_sites
from settings import logger, settings
from spiders.forum_spider import ForumSpider


def spider_job() -> None:
    request_sites = setting_sites.get_next_updates()
    logger.info(f"spider job size: {len(request_sites)}")
    if len(request_sites) <= 0:
        return
    ForumSpider(request_sites=setting_sites.get_next_updates()).start()


def update_sites_job() -> None:
    setting_sites.update_sites()


class SpiderScheduler:
    def __init__(self) -> None:
        _interval_task = {
            "jobstores": {"default": MemoryJobStore()},
            "executors": {
                "default": {"type": "threadpool", "max_workers": 8},
                "processpool": ProcessPoolExecutor(max_workers=5),
            },
            "job_defaults": {
                "coalesce": False,
                "max_instances": 1,
                "misfire_grace_time": 3600,
            },
        }
        self._scheduler = BlockingScheduler(**_interval_task)

    def start(self):
        update_sites_job()
        self._scheduler.add_job(
            spider_job,
            "interval",
            seconds=settings.scheduler_trigger,
            id="spider_job",
            replace_existing=False,
        )
        self._scheduler.start()


class SchedulerTestCase(unittest.TestCase):
    def test_schedule(self):
        schedule = SpiderScheduler()
        schedule.start()

    def test_spider_job(self):
        spider_job()


if __name__ == "__main__":
    unittest.main()
