"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-03
"""
from pydantic import BaseSettings

from settings import settings


class SettingsSpider(BaseSettings):
    feapder_settings = dict(
        ITEM_PIPELINES=["feapder_pipelines.pipelines.pgsql_pipeline.PgsqlPipeline"],
        SPIDER_MAX_RETRY_TIMES=0,
        SPIDER_THREAD_COUNT=settings.spider_thread_count,
        PGSQL_IP=settings.pgsql_ip,
        PGSQL_PORT=settings.pgsql_port,
        PGSQL_DB=settings.pgsql_db,
        PGSQL_USER_NAME=settings.pgsql_user_name,
        PGSQL_USER_PASS=settings.pgsql_user_pass,
        LOG_LEVEL="INFO",
        REQUEST_TIMEOUT=2,
    )


settings_spider = SettingsSpider()
