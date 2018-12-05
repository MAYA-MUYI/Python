import re
import requests

if __name__ == '__main__':
    url = "http://www.heibanke.com/lesson/crawler_ex02/"
    url_login = "http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex02/"

    session = requests.Session()
    session.get(url_login)
    token = session.cookies['csrftoken']
    session.post(url_login, data={"username": "ncjnyzmhsz", "password": "aaaaaa", "csrfmiddlewaretoken": token})
    for number in range(1, 31):
        session.get(url)
        token = session.cookies['csrftoken']
        html = session.post(url, data={"username": "test", "password": number, "csrfmiddlewaretoken": token}).text

        result = re.findall('您输入的密码错误, 请重新输入', html)
        if result:
            print("密码%s错误" %number)
        else:
            print('用户test闯关成功，下一关网址是：http://www.heibanke.com'  + re.findall('<a href="(.*?)" class="btn btn-primary">下一关</a>', html)[0])
            print("密码是：%s" % number)
            break