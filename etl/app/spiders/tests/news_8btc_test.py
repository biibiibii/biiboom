"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-03
"""
import unittest

import requests

headers = {
    "authority": "gate.8btc.cn:8443",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6,de;q=0.5",
    "app-code": "8btc",
    "authorization": '{"secretKeyVersion":1,"sign":"gDt1nQ3Ay458FG_Xj-Aum9YQWV86mZscncBDpiBylO-CtknV2Bu-KrCMiIsFMhORTWeDNrlOJirimPSo2PO0DQ=="}',
    "content-type": "application/json",
    "device_id": "CyPgvDsT146tC8Jg9cEn",
    "from": "web",
    "origin": "https://www.8btc.com",
    "referer": "https://www.8btc.com/",
    "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
}

json_data = {
    "operationName": "listArticle",
    "variables": {
        "first": 20,
        "offset": 60,
        "informationFlow": True,
    },
    "query": "query listArticle($first: Int = 20, $offset: Int, $category: Int, $tag: Int, $informationFlow: Boolean, $country: String) {\n  articleGraph {\n    list: listArticle(page: {first: $first, offset: $offset, pattern: OFFSET}, param: {categoryId: $category, tagId: $tag, country: $country, informationFlow: $informationFlow}) {\n      ...articleListFragment\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment articleListFragment on BaseArticleConnection {\n  edges {\n    node {\n      id\n      template\n      post {\n        title\n        thumbnail\n        desc\n        postDate\n        isOriginal\n        __typename\n      }\n      extra {\n        stat {\n          views\n          __typename\n        }\n        tags {\n          name\n          termId\n          slug\n          taxonomy\n          __typename\n        }\n        source {\n          link\n          name\n          __typename\n        }\n        authorInfo {\n          id\n          uid\n          base {\n            displayName\n            avatar\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on Venture {\n        meta {\n          cat\n          amount\n          round\n          area\n          investors\n          date\n          project\n          __typename\n        }\n        __typename\n      }\n      ... on Weekly {\n        weeklyNum\n        __typename\n      }\n      ... on Special {\n        themeNum\n        __typename\n      }\n      ... on Policy {\n        country\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  pageInfo {\n    totalCount\n    __typename\n  }\n  __typename\n}\n",
}

response = requests.post(
    "https://gate.8btc.cn:8443/one-graph-auth/graphql", headers=headers, json=json_data
)

print(response)
print(len(response.json()["data"]["articleGraph"]["list"]["edges"]))
print(response.json())

if __name__ == "__main__":
    unittest.main()
