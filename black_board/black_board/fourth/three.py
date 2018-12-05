import re
import requests
from threading import Thread
import time

def print_run_time(func):
    """
    装饰器函数，输出运行时间
    """
    def wrapper(self, *args, **kw):
        local_time = time.time()
        # print args),kw
        func(self)
        print('run time is {:.2f}:'.format(time.time() - local_time))
    return wrapper

class hbk_crawler(object):
    """黑板客爬虫闯关"""
    def __init__(self): pass

    def login(self):
        """登录函数 input:第几关"""
        self.url = 'http://www.heibanke.com/lesson/crawler_ex03'
        self.login_url = 'http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex03'
        self.s = requests.session()
        print("正在登录第4关....")
        try:
            self.csrftoken = self.s.get(self.login_url).cookies['csrftoken']
        except:
            print("网络连接错误，请重试...")
            exit()
        self.payload = {'username': 'test', 'password': 'test123',
                        'csrfmiddlewaretoken': self.csrftoken}
        self.payload['csrfmiddlewaretoken'] = self.s.post(
            self.login_url, self.payload).cookies['csrftoken']
        print("登录成功....")
        return None

    def parseurl(self, url):
        """分析网页,查找密码位置和值"""
        while self.count < 100:
            response = self.s.get(url)
            if response.ok:
                content = response.text
                pos_pattern = r'_pos.>(.*)</td>'
                val_pattern = r'_val.>(.*)</td>'
                pos_list = re.findall(pos_pattern, content)
                val_list = re.findall(val_pattern, content)
                for pos, val in zip(pos_list, val_list):
                    if pos not in self.pw_dict:
                        self.pw_dict[pos] = val
                        self.count = self.count + 1
                print(str(self.count) + '%' + self.count // 2 * '*')

    def ex04(self, *args, **kw):
        """ 第4关:找密码,加入了登录验证,CSRF保护,密码长度100位，响应时间增加 """
        self.count = 0
        self.login()
        self.pw_dict = {}
        pw_url = ('http://www.heibanke.com/lesson/crawler_ex03/pw_list',)
        # 线程数,黑板客服务器15秒内最多响应2个请求，否则返回404.
        n = 2
        threads = [Thread(target=self.parseurl, args=(
            pw_url)) for i in range(n)]
        for t in threads:
            print(t.name, 'start...')
            t.start()
        for t in threads:
            t.join()
        self.pw_list = ['' for n in range(101)]
        for pos in self.pw_dict.keys():
            self.pw_list[int(pos)] = self.pw_dict[pos]
        password = int(''.join(self.pw_list))
        self.payload['password'] = password
        response = self.s.post(self.url, self.payload)
        pattern = r'<h3>(.*)</h3>'
        result = re.findall(pattern, response.text)
        result2 = re.findall('<a href="(.*?)" class="btn btn-primary">下一关</a>',response.text)
        print(result[0])
        print(result2)


if __name__ == '__main__':
    Hbk_crawler = hbk_crawler()
    Hbk_crawler.ex04()