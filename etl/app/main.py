from app.setting_sites import (
    setting_sites,
)
from app.spiders.forum_spider import ForumSpider

ForumSpider(request_sites=setting_sites.request_sites).start()
