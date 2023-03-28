"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-03
"""
import unittest

import requests

headers = {
    # "authority": "bnbchain.org",
    # "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    # "accept-language": "en-US,en;q=0.9",
    # "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    # "sec-ch-ua-mobile": "?0",
    # "sec-ch-ua-platform": '"macOS"',
    # "sec-fetch-dest": "document",
    # "sec-fetch-mode": "navigate",
    # "sec-fetch-site": "none",
    # "sec-fetch-user": "?1",
    # "upgrade-insecure-requests": "1",
    # "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
}

response = requests.get(
    "https://bnbchain.org/en/blog/page-data/index/page-data.json", headers=headers
)
print(response)
print(response.text)
if __name__ == "__main__":
    unittest.main()
