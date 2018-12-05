import requests
from lxml import etree

se = requests.session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
}
login_url = "http://www.heibanke.com/accounts/login"
url = 'http://www.heibanke.com/lesson/crawler_ex02/'
username = "lichen123"
password = "123kingstone"

res = se.get(url=login_url, headers=headers, timeout=30).text
csrf = se.cookies['csrftoken']
data = {
    "csrfmiddlewaretoken": csrf,
    "username": username,
    "password": password
}
se.post(url=login_url, headers=headers, data=data, timeout=30)

se.get(url, headers=headers, timeout=30)

# 获取csrf
csrf = se.cookies['csrftoken']

for pwd in range(1, 31):

    data = {
        "csrfmiddlewaretoken": csrf,
        "username": "lichen",
        "password": str(pwd)
    }
    res = se.post(url, headers=headers, data=data, timeout=30).text

    tree = etree.HTML(res)
    h3 = tree.xpath('/html/body/div/div/div[2]/h3/text()')[0]
    hre = tree.xpath('/html/body/div/div/div[2]/a/@href')
    if not u'错误' in h3:
        print(h3)
        print("密码是:%s" %pwd)
        print("下一关地址：http://www.heibanke.com%s" %hre[0])
        break
    else:
        print('密码{}错误'.format(pwd))