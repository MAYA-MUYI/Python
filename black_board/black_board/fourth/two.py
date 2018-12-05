#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-02 22:25:21
# @Author  : bb (317716008@qq.com)
# @Word    : python can change world!
# @Version : python3.6
import requests
from bs4 import BeautifulSoup
import threading
from queue import Queue


dict1={}
vlauess=[]
web1="http://www.heibanke.com/accounts/login"
web2="http://www.heibanke.com/lesson/crawler_ex03/pw_list/"
web3="http://www.heibanke.com/lesson/crawler_ex03/"
global queuewz
global queuemm
queuewz=Queue()
queuemm=Queue()


class mythreads(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        work()
        while not queuemm.empty():
            try:
                dict1[str(queuewz.get())]=queuemm.get()
                print(dict1)
                print("字典长度为%s"%len(dict1))
                if int(len(dict1)) ==100:
                    print("凑到100啦！")
                    for i in range(1,101):
                        vlauess.append(dict1[str(i)])
                    c=vlauess[:100]
                    zzmm=''.join(c)
                    print("密码为%s"%zzmm)
                    print("正在登录.......")
                    dataWebsite1 = {'username': 'user','password': zzmm}
                    s=login_get()
                    res=s.post(web3, data=dataWebsite1).text
                    if u'恭喜' in res:
                        title=re.findall("<title>(.*?)</title>",res)
                        word=re.findall("<h1>(.*?)</h1>",res)
                        word2=re.findall("<h3>(.*?)</h3>",res)
                        html=re.findall('<a href="(.*?)" class="btn btn-primary">下一关</a>',res)
                        print('\n'.join([title[0], word[0], word2[0],'下一关地址是','http://www.heibanke.com'+html[0]]))
                        break
                    else:
                        print("网页有问题哦！可以尝试手动将获得的正确密码登入进去哦！")
                        break
                else:
                    main()
            except IndexError:
                print("例表空了,下一页！")


def login_get():
    try:
        s = requests.Session()
        r=s.get(web1)     # 访问登录页面获取登录要用的csrftoken
        token1 = r.cookies['csrftoken']      # 保存csrftoken
        # 将csrftoekn存入字段csrfmiddlewaretoken
        dataWebsite1 = {'username': 'user',
                        'password': 'password',
                        'csrfmiddlewaretoken': token1
                    }
        res=s.post(web1, data=dataWebsite1)
    except KeyError as e:
        pass

    return s

def get_html(s):
    r=s.get(web2)
    res=r.text
    return res

def get_dict(res):

    soup=BeautifulSoup(res,"html.parser")
    for a in soup.find_all('td',attrs={'title':'password_pos'}):
        wz=(a.string)
        queuewz.put(wz)
    for b in soup.find_all('td',attrs={'title':'password_val'}):
        mm=(b.string)
        queuemm.put(mm)

def work():
    res=get_html(s)
    get_dict(res)


def main():
    global s
    s=login_get()
    threads=[]
    threads_count=10

    for i in range(threads_count):
        threads.append(mythreads())

    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()

