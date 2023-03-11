# -*- coding: utf-8 -*-
"""
Created on 2023-03-11 15:58:35
---------
@summary:
---------
@author: xfu
"""

import feapder
from feapder import ArgumentParser

from app.settings import settings


class BatchSpiderTest(feapder.BatchSpider):
    # 自定义数据库，若项目中有setting.py文件，此自定义可删除
    __custom_setting__ = dict(
        REDISDB_IP_PORTS=settings.redisdb_ip_ports,
        REDISDB_USER_PASS=settings.redisdb_user_pass,
        REDISDB_DB=0,
        MYSQL_IP=settings.mysql_ip,
        MYSQL_PORT=settings.mysql_port,
        MYSQL_DB=settings.mysql_db,
        MYSQL_USER_NAME=settings.mysql_user_name,
        MYSQL_USER_PASS=settings.mysql_user_pass,
    )

    def start_requests(self, task):
        id, url = task
        print(id, url)
        yield feapder.Request(url, task_id=id)

    def parse(self, request, response):
        # 提取网站title
        print(response.xpath("//title/text()").extract_first())
        # 提取网站描述
        # print(response.xpath("//meta[@name='description']/@content").extract_first())
        print("网站地址: ", response.url)
        yield {"abc": 1}
        yield self.update_task_batch(request.task_id, 1)


if __name__ == "__main__":
    spider = BatchSpiderTest(
        redis_key="feapder:test_batch_spider",  # 分布式爬虫调度信息存储位置
        task_table="batch_spider_task",  # mysql中的任务表
        task_keys=["id", "url"],  # 需要
        task_state="state",  # mysql中任务状态字段
        batch_record_table="batch_spider_batch_record",  # mysql中的批次记录表
        batch_name="batch_test",  # 批次名字
        batch_interval=1 / 1440,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="BatchSpiderTest爬虫")

    parser.add_argument(
        "--start_master",
        action="store_true",
        help="添加任务",
        function=spider.start_monitor_task,
    )
    parser.add_argument(
        "--start_worker", action="store_true", help="启动爬虫", function=spider.start
    )

    parser.start()

    # 直接启动
    spider.start()  # 启动爬虫
    spider.start_monitor_task()  # 添加任务

    # 通过命令行启动
    # python batch_spider_test.py --start_master  # 添加任务
    # python batch_spider_test.py --start_worker  # 启动爬虫
