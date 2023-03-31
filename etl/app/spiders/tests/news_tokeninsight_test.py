"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-03
"""
import unittest

import requests

cookies = {
    # "language_": "zh",
    # "_ga": "GA1.1.1002651471.1677976922",
    # "_hjSessionUser_2957885": "eyJpZCI6IjIwYTBiNDljLTgzMjktNTQ5NS04MzMwLWUzZWM1MmEyZmNlYyIsImNyZWF0ZWQiOjE2Nzc5NzY5MjI5MDYsImV4aXN0aW5nIjp0cnVlfQ==",
    # "language": "cn",
    # "hideCookie": "true",
    # "__gads": "ID=4d61ec754a835dd3-22054e2b8ddc003e:T=1679485497:RT=1679485497:S=ALNI_MYZtES-IlnPi3qB7es2Fdp6qTHzaA",
    # "__cf_bm": "mhUDnwnCN5VyhwagklQowylk01Ad6AdZGbJMlc0Mt2Y-1680266332-0-AeBEMhOS6P+bPMnFsWiuwLYD89PwXXWiaYkQ60IGWMzNKCJ6IE4M8Y+GZfjZmRHZSEd3mdPxPCA0nIuAK038cLg=",
    # "__gpi": "UID=00000bde7e5d3dc0:T=1679485497:RT=1680266334:S=ALNI_MZhA4UKD3jw0rSJu4ygc55oNqTR2A",
    # "_hjIncludedInSessionSample_2957885": "0",
    # "_hjSession_2957885": "eyJpZCI6IjkxNmU4MTdlLTI1Y2UtNGJmYS1iMWVmLWQ5NzcxOTM3OTI2YSIsImNyZWF0ZWQiOjE2ODAyNjYzMzQ0NzgsImluU2FtcGxlIjpmYWxzZX0=",
    # "_hjAbsoluteSessionInProgress": "1",
    # "_ga_3F9MFYLVT6": "GS1.1.1680266333.8.1.1680266396.60.0.0",
}

headers = {
    # "authority": "tokeninsight.com",
    # "accept": "application/json, text/plain, */*",
    # "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6,de;q=0.5",
    # "content-type": "application/json",
    # 'cookie': 'language_=zh; _ga=GA1.1.1002651471.1677976922; _hjSessionUser_2957885=eyJpZCI6IjIwYTBiNDljLTgzMjktNTQ5NS04MzMwLWUzZWM1MmEyZmNlYyIsImNyZWF0ZWQiOjE2Nzc5NzY5MjI5MDYsImV4aXN0aW5nIjp0cnVlfQ==; language=cn; hideCookie=true; __gads=ID=4d61ec754a835dd3-22054e2b8ddc003e:T=1679485497:RT=1679485497:S=ALNI_MYZtES-IlnPi3qB7es2Fdp6qTHzaA; __cf_bm=mhUDnwnCN5VyhwagklQowylk01Ad6AdZGbJMlc0Mt2Y-1680266332-0-AeBEMhOS6P+bPMnFsWiuwLYD89PwXXWiaYkQ60IGWMzNKCJ6IE4M8Y+GZfjZmRHZSEd3mdPxPCA0nIuAK038cLg=; __gpi=UID=00000bde7e5d3dc0:T=1679485497:RT=1680266334:S=ALNI_MZhA4UKD3jw0rSJu4ygc55oNqTR2A; _hjIncludedInSessionSample_2957885=0; _hjSession_2957885=eyJpZCI6IjkxNmU4MTdlLTI1Y2UtNGJmYS1iMWVmLWQ5NzcxOTM3OTI2YSIsImNyZWF0ZWQiOjE2ODAyNjYzMzQ0NzgsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=1; _ga_3F9MFYLVT6=GS1.1.1680266333.8.1.1680266396.60.0.0',
    # "origin": "https://tokeninsight.com",
    # "referer": "https://tokeninsight.com/zh/research",
    # "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    # "sec-ch-ua-mobile": "?0",
    # "sec-ch-ua-platform": '"macOS"',
    # "sec-fetch-dest": "empty",
    # "sec-fetch-mode": "cors",
    # "sec-fetch-site": "same-origin",
    # "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "user-agent": "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
    # "x-requested-with": "XMLHttpRequest",
}

json_data = {
    "current": 1,
    "language": "cn",
    "pageSize": 15,
    "tagId": "",
    "type": 0,
}
print(json_data)
response = requests.post(
    "https://tokeninsight.com/apiv2/research/articleList",
    # cookies=cookies,
    headers=headers,
    json=json_data,
)
print(response)
print(response.json())

if __name__ == "__main__":
    unittest.main()
