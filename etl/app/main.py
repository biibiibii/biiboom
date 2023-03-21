from app.setting_sites import make_forum_requests, make_chainfeeds_request
from app.spiders.forum_spider import ForumSpider

ForumSpider(request_sites=make_forum_requests()).start()
ForumSpider(request_sites=make_chainfeeds_request()).start()
