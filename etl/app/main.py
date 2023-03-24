from setting_sites import setting_sites
from spiders.forum_spider import ForumSpider

ForumSpider(request_sites=setting_sites.request_sites).start()
