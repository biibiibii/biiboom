from setting_rules import setting_rules
from setting_sites import setting_sites
from spiders.forum_spider import ForumSpider

setting_rules.update_rules()
setting_sites.update_sites()
ForumSpider(request_sites=setting_sites.request_sites).start()
