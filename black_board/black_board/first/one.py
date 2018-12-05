import requests
import re
from lxml import etree

def get_Html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36"
    }
    req = requests.get(url, headers=headers, timeout=20)
    # print(req.content.decode('utf-8'))
    return req.content.decode('utf-8')

def next():
    html = get_Html(url)
    number = re.findall('<h3>.*?(\d+)</h3>', html)
    while number:
        next_url = "http://www.heibanke.com/lesson/crawler_ex00/%s" % number[0]
        print(next_url)
        html = requests.get(next_url).content.decode('utf-8')
        number = re.findall(r'<h3>.*?(\d+)\.', html)
    res = re.findall('<a href="(.*?)" class', html)
    print("下一关的连接：http://www.heibanke.com:%s" %res[0])


if __name__ == '__main__':
    url = "http://www.heibanke.com/lesson/crawler_ex00/"
    next()
