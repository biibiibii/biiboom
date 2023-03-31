"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-03
"""
import unittest

import requests

headers = {
    # "authority": "api2.bybit.com",
    # "accept": "application/json, text/plain, */*",
    # "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6,de;q=0.5",
    # "content-type": "application/json",
    "origin": "https://announcements.bybit.com",
    "referer": "https://announcements.bybit.com/",
    # "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    # "sec-ch-ua-mobile": "?0",
    # "sec-ch-ua-platform": '"macOS"',
    # "sec-fetch-dest": "empty",
    # "sec-fetch-mode": "cors",
    # "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
}

json_data = {
    "data": {
        "query": "",
        "page": 0,
        "hitsPerPage": 20,
        "filters": "category.key: 'new_crypto'",
    },
}

response = requests.post(
    "https://api2.bybit.com/announcements/api/search/v1/index/announcement-posts_en-us",
    headers=headers,
    json=json_data,
)

print(response)
print(response.json())
print(len(response.json()["result"]["hits"]))
if __name__ == "__main__":
    unittest.main()
