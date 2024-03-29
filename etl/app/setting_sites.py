"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-03
"""
import unittest

from playhouse.shortcuts import model_to_dict
from pydantic import BaseSettings

from db.item_client import item_client
from db.items import RequestSite, Site, MatchRule, SiteLanguageEnum, SiteTagsEnum
from db.model import SiteModel
from setting_rules import setting_rules
from settings import settings, logger
from spiders.forum_spider import ForumSpider
from utils import Utils

__all__ = ["setting_sites"]


def build_forum_request(url: str) -> RequestSite:
    rule = setting_rules.rule_forum
    site = Site.get_or_create(
        url=f"{url}/latest.json?no_definitions=true&page=0",
        jump_base_url=f"{url}/t/",
        original_url=f"{url}/latest/",
        rule_id=rule.id,
        language=SiteLanguageEnum.EN.value,
        name=Utils.get_name_from_url(url),
        sub_name="Forum",
        tags=[SiteTagsEnum.FORUM.value],
    )
    return RequestSite(site=site, rule=rule)


def make_forum_requests() -> list[RequestSite]:
    url_list = settings.forum_urls
    return [build_forum_request(item) for item in url_list]


def make_news_chainfeeds_request() -> list[RequestSite]:
    url_list = settings.news_cn_urls
    rule = setting_rules.rule_news_chainfeeds
    sites = [
        Site.get_or_create(
            url=f"https://api.chainfeeds.xyz/feed/list?page=1&page_size=20&group_alias=selected",
            jump_base_url=f"https://www.chainfeeds.xyz/feed/detail/",
            original_url=f"{item}/",
            rule_id=rule.id,
            language=SiteLanguageEnum.ZH.value,
            name=Utils.get_name_from_url(item),
            sub_name="发现",
            tags=[SiteTagsEnum.NEWS.value],
        )
        for item in url_list
    ]
    return [RequestSite(site=site, rule=rule) for site in sites]


def make_news_marbits_request() -> list[RequestSite]:
    rule = setting_rules.rule_news_marsbit
    item_client.save_item(rule)
    original_url = "https://www.marsbit.co/"
    site = Site.get_or_create(
        url=f"https://api.marsbit.co/info/news/shownews",
        jump_base_url="https://news.marsbit.co/{id}.html",
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.ZH.value,
        name=Utils.get_name_from_url(original_url),
        sub_name="新闻",
        tags=[SiteTagsEnum.NEWS.value],
    )
    item_client.save_item(site)
    return [RequestSite(site=site, rule=rule)]


def make_news_odaily_request() -> list[RequestSite]:
    rule = setting_rules.rule_news_odaily
    item_client.save_item(rule)
    original_url = "https://www.odaily.news/"
    site = Site.get_or_create(
        url=f"https://www.odaily.news/api/pp/api/app-front/feed-stream?feed_id=280&b_id=&per_page=50",
        jump_base_url="https://www.odaily.news/post/",
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.ZH.value,
        name=Utils.get_name_from_url(original_url),
        sub_name="新闻",
        tags=[SiteTagsEnum.NEWS.value],
    )
    item_client.save_item(site)
    return [RequestSite(site=site, rule=rule)]


def make_news_wutalk_request() -> list[RequestSite]:
    rule = setting_rules.rule_news_wutalk
    original_url = "https://www.wu-talk.com/"
    site = Site.get_or_create(
        url=f"https://api.wu-talk.com/api/site/getAllArticleList",
        jump_base_url="",
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.ZH.value,
        name="吴说",
        sub_name="",
        tags=[SiteTagsEnum.NEWS.value],
        request_method="post",
        request_data={
            "pageIndex": "1",
            "pageSize": "50",
        },
    )
    return [RequestSite(site=site, rule=rule)]


def make_news_panews_request() -> list[RequestSite]:
    rule = setting_rules.rule_news_panews
    original_url = "https://www.panewslab.com/zh/index.html"
    site = Site.get_or_create(
        url=f"https://www.panewslab.com/webapi/index/list?Rn=30&LId=1&LastTime=",
        jump_base_url="https://www.panewslab.com/zh/articledetails/{id}.html",
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.ZH.value,
        name="PaNews",
        sub_name="精选",
        tags=[SiteTagsEnum.NEWS.value],
    )
    return [RequestSite(site=site, rule=rule)]


def make_news_jinse_request() -> list[RequestSite]:
    rule = setting_rules.rule_news_jinse
    item_client.save_item(rule)
    original_url = "https://www.jinse.com/"
    site = Site.get_or_create(
        url=f"https://api.jinse.cn/noah/v3/timelines?catelogue_key=www&limit=50&information_id=&flag=down",
        jump_base_url="",
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.ZH.value,
        name="金色财经",
        sub_name="头条",
        tags=[SiteTagsEnum.NEWS.value],
    )
    item_client.save_item(site)
    return [RequestSite(site=site, rule=rule)]


def make_news_8btc_request() -> list[RequestSite]:
    rule = setting_rules.rule_news_8btc
    item_client.save_item(rule)
    original_url = "https://www.8btc.com/"
    site = Site.get_or_create(
        url=f"https://www.8btc.com/sitemap",
        jump_base_url=original_url,
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.ZH.value,
        name="巴比特",
        sub_name="资讯",
        tags=[SiteTagsEnum.NEWS.value],
    )
    item_client.save_item(site)
    return [RequestSite(site=site, rule=rule)]


def make_news_defidao_request() -> list[RequestSite]:
    rule = setting_rules.rule_news_8btc
    item_client.save_item(rule)
    original_url = "https://www.defidaonews.com/"
    site = Site.get_or_create(
        url=f"https://www.defidaonews.com/sitemap",
        jump_base_url=original_url,
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.ZH.value,
        name="DeFi之道",
        sub_name="资讯",
        tags=[SiteTagsEnum.NEWS.value],
    )
    item_client.save_item(site)

    return [RequestSite(site=site, rule=rule)]


def make_news_chaincatcher_request() -> list[RequestSite]:
    rule = setting_rules.rule_news_chaincatcher
    original_url = "https://www.chaincatcher.com/"
    site = Site.get_or_create(
        url=f"https://www.chaincatcher.com/api/article/lists",
        jump_base_url="https://www.chaincatcher.com/article/",
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.ZH.value,
        name="链捕手",
        sub_name="资讯",
        tags=[SiteTagsEnum.NEWS.value],
        request_method="post",
        request_data={
            "page": "1",
            "home": "1",
        },
    )
    return [RequestSite(site=site, rule=rule)]


def make_news_blockbeats() -> list[RequestSite]:
    rule = setting_rules.rule_news_blockbeats
    setting_rules.update_rule(rule)

    original_url = "https://www.theblockbeats.info/article"
    site = Site.get_or_create(
        url=f"https://api.theblockbeats.info/v3/Information/newsall?page=1",
        jump_base_url="https://www.theblockbeats.info/news/",
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.ZH.value,
        name="律动",
        sub_name="文章",
        tags=[SiteTagsEnum.NEWS.value],
    )
    return [RequestSite(site=site, rule=rule)]


def make_news_blockbeats_flash() -> list[RequestSite]:
    rule = setting_rules.rule_news_blockbeats_flash
    item_client.save_item(rule)

    original_url = "https://www.theblockbeats.info/newsflash"
    site = Site.get_or_create(
        url=f"https://api.theblockbeats.info/v3/newsflash/select?page=1",
        jump_base_url="https://www.theblockbeats.info/flash/",
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.ZH.value,
        name="律动",
        sub_name="快讯",
        tags=[SiteTagsEnum.NEWS.value],
    )
    item_client.save_item(site)
    return [RequestSite(site=site, rule=rule)]


def make_news_tokeningisht_request() -> list[RequestSite]:
    rule = setting_rules.rule_news_tokeninsight
    item_client.save_item(rule)

    original_url = "https://tokeninsight.com/zh/research"
    site = Site.get_or_create(
        url=f"https://tokeninsight.com/apiv2/research/articleList",
        jump_base_url="https://tokeninsight.com/zh/research/daily-digest/",
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.ZH.value,
        name="TokenInsight",
        sub_name="研究",
        tags=[SiteTagsEnum.NEWS.value],
        request_method="post",
        request_data={
            "current": 1,
            "language": "cn",
            "pageSize": 15,
            "tagId": "",
            "type": 0,
        },
    )
    item_client.save_item(site)

    return [RequestSite(site=site, rule=rule)]


def make_cex_binance_news() -> list[RequestSite]:
    rule = setting_rules.rule_cex_binance_news
    item_client.save_item(rule)

    original_url = "https://www.binance.com/en/support/announcement/latest-binance-news?c=49&navId=49"
    site = Site.get_or_create(
        url=f"https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&pageSize=20&pageNo=1",
        jump_base_url="https://www.binance.com/en/support/announcement/",
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.EN.value,
        name="Binance",
        sub_name="Latest News",
        tags=[SiteTagsEnum.CEX.value],
    )
    item_client.save_item(site)
    return [RequestSite(site=site, rule=rule)]


def make_cex_binance_token_listing() -> list[RequestSite]:
    rule = setting_rules.rule_cex_binance_tokenlisting
    item_client.save_item(rule)

    original_url = "https://www.binance.com/en/support/announcement/new-cryptocurrency-listing?c=48&navId=48"
    site = Site.get_or_create(
        url=f"https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&pageSize=15&pageNo=1",
        jump_base_url="https://www.binance.com/en/support/announcement/",
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.EN.value,
        name="Binance",
        sub_name="Token Listing",
        tags=[SiteTagsEnum.CEX.value],
    )
    item_client.save_item(site)
    return [RequestSite(site=site, rule=rule)]


def make_cex_okx_news() -> list[RequestSite]:
    rule = setting_rules.rule_cex_okx_news
    item_client.save_item(rule)

    original_url = "https://www.okx.com/help-center/section/latest-announcements"
    site = Site.get_or_create(
        url=f"https://www.okx.com/v2/support/home/web",
        jump_base_url="",
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.EN.value,
        name="OKX",
        sub_name="Latest News",
        tags=[SiteTagsEnum.CEX.value],
    )
    item_client.save_item(site)
    return [RequestSite(site=site, rule=rule)]


def make_cex_kucoin_announcements() -> list[RequestSite]:
    rule = setting_rules.rule_cex_kucoin_announcements
    item_client.save_item(rule)

    original_url = "https://www.kucoin.com/news/categories/announcements"
    site = Site.get_or_create(
        url=f"https://www.kucoin.com/_api/cms/articles?category=announcements&lang=en_US&page=1&pageSize=20",
        jump_base_url="https://www.kucoin.com/news",
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.EN.value,
        name="KuCoin",
        sub_name="Announcements",
        tags=[SiteTagsEnum.CEX.value],
    )
    item_client.save_item(site)
    return [RequestSite(site=site, rule=rule)]


def make_cex_kucoin_token_listing() -> list[RequestSite]:
    rule = setting_rules.rule_cex_kucoin_announcements
    item_client.save_item(rule)

    original_url = "https://www.kucoin.com/news/categories/listing"
    site = Site.get_or_create(
        url=f"https://www.kucoin.com/_api/cms/articles?category=listing&lang=en_US&page=1&pageSize=20",
        jump_base_url="https://www.kucoin.com/news",
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.EN.value,
        name="KuCoin",
        sub_name="Token Listing",
        tags=[SiteTagsEnum.CEX.value],
    )
    item_client.save_item(site)
    return [RequestSite(site=site, rule=rule)]


def make_cex_kucoin_news() -> list[RequestSite]:
    rule = setting_rules.rule_cex_kucoin_announcements
    item_client.save_item(rule)

    original_url = "https://www.kucoin.com/news/categories/news"
    site = Site.get_or_create(
        url=f"https://www.kucoin.com/_api/cms/articles?category=news&lang=en_US&page=1&pageSize=20",
        jump_base_url="https://www.kucoin.com/news",
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.EN.value,
        name="KuCoin",
        sub_name="News",
        tags=[SiteTagsEnum.CEX.value],
    )
    item_client.save_item(site)
    return [RequestSite(site=site, rule=rule)]


def make_cex_mexc_announcements() -> list[RequestSite]:
    rule = setting_rules.rule_cex_mexc_announcements
    item_client.save_item(rule)
    section_id = "360000679912"
    original_url = f"https://www.mexc.com/support/sections/{section_id}"
    site = Site.get_or_create(
        url=f"https://www.mexc.com/help/announce/api/en-001/sections/{section_id}/articles?page=1&per_page=30",
        jump_base_url="https://www.mexc.com/support/articles/",
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.EN.value,
        name="Mexc",
        sub_name="Announcements",
        tags=[SiteTagsEnum.CEX.value],
    )
    item_client.save_item(site)
    return [RequestSite(site=site, rule=rule)]


def make_cex_mexc_token_listing() -> list[RequestSite]:
    rule = setting_rules.rule_cex_mexc_announcements
    item_client.save_item(rule)
    section_id = "360000547811"
    original_url = f"https://www.mexc.com/support/sections/{section_id}"
    site = Site.get_or_create(
        url=f"https://www.mexc.com/help/announce/api/en-001/sections/{section_id}/articles?page=1&per_page=30",
        jump_base_url="https://www.mexc.com/support/articles/",
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.EN.value,
        name="Mexc",
        sub_name="Token Listing",
        tags=[SiteTagsEnum.CEX.value],
    )
    item_client.save_item(site)
    return [RequestSite(site=site, rule=rule)]


def make_blog_bnbchain_request() -> list[RequestSite]:
    rule = setting_rules.rule_blog_bnbchain
    item_client.save_item(rule)
    original_url = "https://bnbchain.org/en/blog/"
    site = Site.get_or_create(
        url=f"https://bnbchain.org/en/blog/page-data/index/page-data.json",
        jump_base_url="https://bnbchain.org/en/blog/",
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.EN.value,
        name=Utils.get_name_from_url(original_url),
        sub_name="blog",
        tags=[SiteTagsEnum.BLOG.value],
    )
    return [RequestSite(site=site, rule=rule)]


def make_blog_binance_request() -> list[RequestSite]:
    rule = setting_rules.rule_blog_binance
    item_client.save_item(rule)
    original_url = "https://www.binance.com/en/blog"
    site = Site.get_or_create(
        url=f"https://www.binance.com/bapi/composite/v1/public/content/blog/list?category=&tag=&page=1&size=20",
        jump_base_url="https://www.binance.com/en/blog/a/",
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.EN.value,
        name=Utils.get_name_from_url(original_url),
        sub_name="blog",
        tags=[SiteTagsEnum.BLOG.value],
    )
    return [RequestSite(site=site, rule=rule)]


def make_blog_kucoin_request() -> list[RequestSite]:
    rule = setting_rules.rule_cex_kucoin_announcements
    item_client.save_item(rule)

    original_url = "https://www.kucoin.com/blog"
    site = Site.get_or_create(
        url=f"https://www.kucoin.com/_api/cms/articles?page=1&pageSize=20&type=3&lang=en_US",
        jump_base_url="https://www.kucoin.com/blog",
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.EN.value,
        name="KuCoin",
        sub_name="Blog",
        tags=[SiteTagsEnum.BLOG.value],
    )
    item_client.save_item(site)
    return [RequestSite(site=site, rule=rule)]


def make_blog_polkadot_request() -> list[RequestSite]:
    rule = setting_rules.rule_blog_polkadot
    item_client.save_item(rule)

    original_url = "https://polkadot.network/blog/"
    site = Site.get_or_create(
        url=f"https://polkadot.network/page-data/blog/page-data.json",
        jump_base_url="https://polkadot.network/blog/",
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.EN.value,
        name=Utils.get_name_from_url(original_url),
        sub_name="Blog",
        tags=[SiteTagsEnum.BLOG.value],
    )
    item_client.save_item(site)
    return [RequestSite(site=site, rule=rule)]


def make_blog_ethereum_request() -> list[RequestSite]:
    rule = setting_rules.rule_blog_ethereum
    item_client.save_item(rule)
    # Get json data by html
    original_url = "https://blog.ethereum.org/"
    site = Site.get_or_create(
        url=f"https://blog.ethereum.org/_next/data/B4tauPzc7B80ozj3si_al/en.json",
        jump_base_url=original_url,
        original_url=original_url,
        rule_id=rule.id,
        language=SiteLanguageEnum.EN.value,
        sub_name="blog",
        tags=[SiteTagsEnum.BLOG.value],
    )
    return [RequestSite(site=site, rule=rule)]


class SettingSites(BaseSettings):
    @classmethod
    def get_next_updates(cls) -> list[RequestSite]:
        update_sites = SiteModel.select_next_updates()
        return cls.to_request_sites(update_sites)

    @classmethod
    def to_request_sites(cls, site_models: list[SiteModel]) -> list[RequestSite]:
        __site_list = []
        for item in site_models:
            item.rule_id = item.rule.id
            item_dict = model_to_dict(item, backrefs=False)
            if "rule" in item_dict:
                del item_dict["rule"]
            item_dict["rule_id"] = item.rule_id
            __site_list.append(
                RequestSite(
                    site=Site(**item_dict),
                    rule=MatchRule(**model_to_dict(item.rule)),
                )
            )

        return __site_list


setting_sites = SettingSites()


class SiteModelTestCase(unittest.TestCase):
    def test_site_model(self):
        # setting_sites.update_sites()
        req = make_news_marbits_request()
        logger.debug(f"site_model: {req}")
        pass


class RequestsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        # setting_sites.update_sites()
        pass

    def test_get_next_updates(self):
        next_updates = setting_sites.get_next_updates()
        logger.debug(f"updates: {next_updates}")

    def test_forum_near(self):
        req = build_forum_request("https://gov.near.org")
        ForumSpider(request_sites=[req]).start()

    def test_chainfeeds(self):
        feeds = make_news_chainfeeds_request()
        ForumSpider(request_sites=feeds).start()
        pass

    def test_marsbit(self):
        marsbit = make_news_marbits_request()
        ForumSpider(request_sites=marsbit).start()

    def test_news_odaily(self):
        odaily = make_news_odaily_request()
        ForumSpider(request_sites=odaily).start()

    def test_news_wutalk(self):
        req = make_news_wutalk_request()
        ForumSpider(request_sites=req).start()

    def test_news_wutalk_1(self):
        site_id = "bb246159cfc93001c0563ee62fd880d072e8a560c84585f1c60262d744aaeba5"
        site_model = SiteModel.get_by_id(site_id)
        site_dict = model_to_dict(site_model)
        logger.debug(f"site dict: {site_dict}")
        reqs = setting_sites.to_request_sites([site_model])
        logger.debug(f"request sites: {reqs}")
        ForumSpider(request_sites=reqs).start()

    def test_news_panews(self):
        req = make_news_panews_request()
        ForumSpider(request_sites=req).start()

    def test_news_jinse(self):
        req = make_news_jinse_request()
        ForumSpider(request_sites=req).start()

    def test_news_8btc(self):
        req = make_news_8btc_request()
        ForumSpider(request_sites=req).start()

    def test_news_defidao(self):
        req = make_news_defidao_request()
        ForumSpider(request_sites=req).start()

    def test_news_chaincatcher(self):
        req = make_news_chaincatcher_request()
        ForumSpider(request_sites=req).start()

    def test_news_blockbeats(self):
        req = make_news_blockbeats()
        ForumSpider(request_sites=req).start()

    def test_news_blockbeats_flash(self):
        req = make_news_blockbeats_flash()
        ForumSpider(request_sites=req).start()

    def test_news_tokeninsight(self):
        req = make_news_tokeningisht_request()
        ForumSpider(request_sites=req).start()

    def test_cex_binance_news(self):
        req = make_cex_binance_news()
        ForumSpider(request_sites=req).start()

    def test_cex_binance_token_listing(self):
        req = make_cex_binance_token_listing()
        ForumSpider(request_sites=req).start()

    def test_cex_okx_news(self):
        req = make_cex_okx_news()
        ForumSpider(request_sites=req).start()

    def test_cex_kucoin_announcements(self):
        req = make_cex_kucoin_announcements()
        ForumSpider(request_sites=req).start()

    def test_cex_kucoin_token_listing(self):
        req = make_cex_kucoin_token_listing()
        ForumSpider(request_sites=req).start()

    def test_cex_kucoin_news(self):
        req = make_cex_kucoin_news()
        ForumSpider(request_sites=req).start()

    def test_cex_mexc_announcements(self):
        req = make_cex_mexc_announcements()
        ForumSpider(request_sites=req).start()

    def test_cex_mexc_token_listing(self):
        req = make_cex_mexc_token_listing()
        ForumSpider(request_sites=req).start()

    def test_bnbchain_blog(self):
        bnbchain_blog = make_blog_bnbchain_request()
        ForumSpider(request_sites=bnbchain_blog).start()

    def test_ethereum_blog(self):
        ethereum = make_blog_ethereum_request()
        ForumSpider(request_sites=ethereum).start()

    def test_binance_blog(self):
        req = make_blog_binance_request()
        ForumSpider(request_sites=req).start()

    def test_kucoin_blog(self):
        req = make_blog_kucoin_request()
        ForumSpider(request_sites=req).start()

    def test_polkadot_blog(self):
        req = make_blog_polkadot_request()
        ForumSpider(request_sites=req).start()


if __name__ == "__main__":
    unittest.main()
