"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-03
"""
import unittest

import requests

headers = {
    "authority": "api.wu-talk.com",
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6,de;q=0.5",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://www.wu-talk.com",
    "referer": "https://www.wu-talk.com/",
    "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
}

data = {
    "pageIndex": "1",
    "pageSize": "50",
}

response = requests.post(
    "https://api.wu-talk.com/api/site/getAllArticleList", headers=headers, data=data
)
print(response)
print(len(response.json()["data"]))
print(response.json())

if __name__ == "__main__":
    unittest.main()
