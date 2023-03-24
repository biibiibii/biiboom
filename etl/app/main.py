from scheduler import SpiderScheduler
from settings import logger

logger.info("start scheduler...")
schedule = SpiderScheduler()
schedule.start()
