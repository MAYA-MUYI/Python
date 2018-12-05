import requests
from lxml import etree
import codecs
import csv
import re


se = requests.session()


headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
}

class HBK():
    def __init__(self):
        self.login_url = "http://www.heibanke.com/accounts/login"
        self.username = "whaike"
        self.password = "12345654321"
        self.passwrods = ['' for i in range(101)]
        self.pwd = ''

        ##获取登陆之前的csrf
    def getCsrf(self):
        res = se.get(url=self.login_url,headers=headers,timeout=30).text
        tree = etree.HTML(res)
        self.csrf = tree.xpath('/html/body/div/div/div[2]/form/input[@name="csrfmiddlewaretoken"]/@value')[0]

    #登陆
    def login(self):
        self.getCsrf()
        data = {
            "csrfmiddlewaretoken":self.csrf,
            "username":self.username,
            "password":self.password
        }
        se.post(url=self.login_url,headers=headers,data=data,timeout=30)
        print('登陆成功')

    #获取登陆之后的csrf,也就是要进行第四关闯关的csrf
    def getNCsrf(self):
        url = 'http://www.heibanke.com/lesson/crawler_ex03/'
        res = se.get(url,headers=headers,timeout=30).text
        tree = etree.HTML(res)
        csrf = tree.xpath('//input[1]/@value')[0]
        return csrf

    #猜测密码是否正确
    def guesspwd(self):
        url = 'http://www.heibanke.com/lesson/crawler_ex03/'
        csrf = self.getNCsrf()
        data = {
            "csrfmiddlewaretoken":csrf,
            "username":"whaike",
            "password":self.pwd
        }
        res = se.post(url,headers=headers,data=data,timeout=30)
        if int(res.status_code) == 200:
            self.h3 = re.findall('<h3>(.*?)</h3>',res.text)
            return True
        else:
            return False

    #循环抓取第一页的随机值，直到密码长度为100时开始猜测，猜测失败继续执行，猜测成功停止运行
    def getGasswords(self):
        print('获取第一页')
        url = 'http://www.heibanke.com/lesson/crawler_ex03/pw_list/?page=1'
        res = se.get(url,headers=headers,timeout=30).text
        tree = etree.HTML(res)
        trs = tree.xpath('/html/body/div/div/div[2]/table/tr')[1:]
        for tr in trs:
            p1 = tr.xpath('td[1]/text()')[0] #位置
            p = int(re.findall('\d+',p1)[0]) #偶尔数字前会有一些其他字符出现,提取数字部分,转换为整数
            w = tr.xpath('td[2]/text()')[0] #值
            self.passwrods[p] = w
        self.pwd = ''.join(self.passwrods)
        length = len(self.pwd) #密码长度
        print('当前密码:%s,长度%d'%(self.pwd,length))
        if length == 100:
            print('满足条件，开始猜测...')
            if self.guesspwd():
                print ('猜测成功,密码为:%s'%self.pwd)
            else:
                print ('猜测失败,继续执行')
                self.getGasswords()
        else: #如果密码长度不为100，则再次获取第一页的随机密码并组成新的密码
            self.getGasswords() #递归


if __name__ == '__main__':

    print('开始闯关 - 第四关')
    spider = HBK()
    spider.login()
    spider.getGasswords()
    print(spider.h3)