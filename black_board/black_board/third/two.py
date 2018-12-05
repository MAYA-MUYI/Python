import requests
import re


def main():
    login_data = {'username': 'user', 'password': 'password'}
    url = 'http://www.heibanke.com/lesson/crawler_ex02/'
    login_url = 'http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex02/'
    r2 = requests.get(login_url)
    c2 = r2.cookies
    login_data['csrfmiddlewaretoken'] = c2['csrftoken']
    r3 = requests.post(login_url, data=login_data, allow_redirects=False, cookies=c2)
    c3 = r3.cookies
    pass_data = {'username': 'user', 'csrfmiddlewaretoken': c3['csrftoken']}
    for passwd in range(31):
        pass_data['password'] = passwd
        r5 = requests.post(url, pass_data, cookies=c3)
        text = r5.text
        result = re.findall(r'密码错误', text)
        if u'密码错误' in text:
            print("%s密码错误" % passwd)
        else:
            print("%s密码正确" % passwd)
            title = re.findall("<title>(.*?)</title>", text)
            word = re.findall("<h1>(.*?)</h1>", text)
            word2 = re.findall("<h3>(.*?)</h3>", text)
            html = re.findall('<a href="(.*?)" class="btn btn-primary">下一关</a>', text)
            print('\n'.join([title[0], word[0], word2[0], '下一关地址是', 'http://www.heibanke.com' + html[0]]))
            break


if __name__ == '__main__':
    main()
