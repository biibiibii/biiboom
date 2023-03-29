"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-03
"""
import unittest

import requests

cookies = {
    # "PHPSESSID": "fgjv8t8dviutgmnpqvpoejhfi6",
    # "_ga": "GA1.1.1908251090.1679730080",
    # "think_var": "en-us",
    # "_ga_6MSXXZNH3G": "GS1.1.1680096071.4.0.1680096077.0.0.0",
}

headers = {
    # "Accept": "*/*",
    # "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6,de;q=0.5",
    # "Connection": "keep-alive",
    # "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    # # 'Cookie': 'PHPSESSID=fgjv8t8dviutgmnpqvpoejhfi6; _ga=GA1.1.1908251090.1679730080; think_var=en-us; _ga_6MSXXZNH3G=GS1.1.1680096071.4.0.1680096077.0.0.0',
    # "Origin": "https://www.chaincatcher.com",
    # "Referer": "https://www.chaincatcher.com/",
    # "Sec-Fetch-Dest": "empty",
    # "Sec-Fetch-Mode": "cors",
    # "Sec-Fetch-Site": "same-origin",
    # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    # "X-Requested-With": "XMLHttpRequest",
    # "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    # "sec-ch-ua-mobile": "?0",
    # "sec-ch-ua-platform": '"macOS"',
}

data = {
    "page": "1",
    "home": "1",
}

response = requests.post(
    "https://www.chaincatcher.com/api/article/lists",
    cookies=cookies,
    headers=headers,
    data=data,
)
print(response)
print(response.json())
print(len(response.json()["data"]))
if __name__ == "__main__":
    unittest.main()
