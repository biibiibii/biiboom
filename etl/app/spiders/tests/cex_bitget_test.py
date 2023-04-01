"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-04
"""
import unittest

import requests

cookies = {
    '_ga': 'GA1.1.925997241.1680274638',
    'BITGET_LOCAL_COOKIE': '{%22bitget_lang%22:%22en%22%2C%22bitget_unit%22:%22USD%22%2C%22bitget_showasset%22:true%2C%22bitget_theme%22:%22black%22%2C%22bitget_layout%22:%22right%22%2C%22bitget_valuationunit%22:1%2C%22bitgt_login%22:false}',
    '_ga_clientid': '925997241.1680274638',
    '_ga_sessionid': '1680274638',
    'bt_sessonid': '',
    'bt_newsessionid': '',
    '_fbp': 'fb.1.1680274648717.1473088996',
    '_tt_enable_cookie': '1',
    '_ttp': '9Yg6sE-HrRS0v5Ek-8SApcUB3E3',
    'afUserId': 'fc938730-58b9-46af-8825-7428f251b55e-p',
    'AF_SYNC': '1680274651202',
    '__zlcmid': '1F9liDV2b7XYuGy',
    'G_ENABLED_IDPS': 'google',
    'bt_rtoken': '',
    '__cf_bm': 'wVSQcW3bEfrmEgxDaNnuLJh_3FFd3uvlv0ulmISi0ME-1680318315-0-Af46sW/M0DFxI41EQLZPowDzqkWQzr7OO6Nh9Y7TtRvTeEDC005ycbE9qNs+Y+RFdEoJNpdWUhVYPJW0EAQZoFk=',
    '_cfuvid': 'hmwQPFpOUGRCAVOszesMRqysrVo123ZBGOyd4LrRPf4-1680318315752-0-604800000',
    'outbrain_cid_fetch': 'true',
    '_ga_Z8Q93KHR0F': 'GS1.1.1680318316.2.1.1680318339.0.0.0',
    '_ga_B8RNGYK5MS': 'GS1.1.1680318316.2.1.1680318339.0.0.0',
}

headers = {
    'authority': 'www.bitget.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6,de;q=0.5',
    'content-type': 'application/json;charset=UTF-8',
    # 'cookie': '_ga=GA1.1.925997241.1680274638; BITGET_LOCAL_COOKIE={%22bitget_lang%22:%22en%22%2C%22bitget_unit%22:%22USD%22%2C%22bitget_showasset%22:true%2C%22bitget_theme%22:%22black%22%2C%22bitget_layout%22:%22right%22%2C%22bitget_valuationunit%22:1%2C%22bitgt_login%22:false}; _ga_clientid=925997241.1680274638; _ga_sessionid=1680274638; bt_sessonid=; bt_newsessionid=; _fbp=fb.1.1680274648717.1473088996; _tt_enable_cookie=1; _ttp=9Yg6sE-HrRS0v5Ek-8SApcUB3E3; afUserId=fc938730-58b9-46af-8825-7428f251b55e-p; AF_SYNC=1680274651202; __zlcmid=1F9liDV2b7XYuGy; G_ENABLED_IDPS=google; bt_rtoken=; __cf_bm=wVSQcW3bEfrmEgxDaNnuLJh_3FFd3uvlv0ulmISi0ME-1680318315-0-Af46sW/M0DFxI41EQLZPowDzqkWQzr7OO6Nh9Y7TtRvTeEDC005ycbE9qNs+Y+RFdEoJNpdWUhVYPJW0EAQZoFk=; _cfuvid=hmwQPFpOUGRCAVOszesMRqysrVo123ZBGOyd4LrRPf4-1680318315752-0-604800000; outbrain_cid_fetch=true; _ga_Z8Q93KHR0F=GS1.1.1680318316.2.1.1680318339.0.0.0; _ga_B8RNGYK5MS=GS1.1.1680318316.2.1.1680318339.0.0.0',
    'language': 'en_US',
    'locale': 'en_US',
    'origin': 'https://www.bitget.com',
    'referer': 'https://www.bitget.com/en/support/sections/360007868532',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'terminaltype': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'website': 'mix',
}

json_data = {
    'pageNum': 1,
    'pageSize': 20,
    'locale': 'en',
    'params': {
        'sectionId': '360007868532',
        'firstSearchTime': 1680318316221,
        'locale': 'en',
        'languageType': 0,
    },
    'languageType': 0,
}

response = requests.post(
    'https://www.bitget.com/v1/cms/helpCenter/content/section/helpContentDetail',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

print(response)
print(response.text)

if __name__ == "__main__":
    unittest.main()
