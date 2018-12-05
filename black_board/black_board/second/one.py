import re
import requests



if __name__ == '__main__':

    data = {'username': 'test'}

    url = 'http://www.heibanke.com/lesson/crawler_ex01/'

    for num in range(1, 31):
        data['password'] = num
        print(data)
        html = requests.post(url,data).content.decode('utf-8')
        result = re.findall('您输入的密码错误, 请重新输入', html)
        if result:
            print("错误")
        else:
            print('闯关成功，下一关网址是：http://www.heibanke.com' + re.findall('<a href="(.*?)" class', html)[0])
            break