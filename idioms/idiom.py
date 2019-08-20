#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@software: Pycharm
@file: idiom.py
@time: 2019/8/14 14:36
@desc:
'''
import requests
import json
from lxml import etree
import re


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3',
    'Upgrade-Insecure-Requests': '1'
}



def get_html(url):
    r = requests.get(url, headers=headers)
    r.encoding = 'gbk'
    return r.text

def get_curr(url):
    html = etree.HTML(get_html(url))
    lis = html.xpath('//li[@class="licontent"]')
    context = {}
    for li in lis:
        if li.xpath('./span[@class="hz"]/a/text()') and li.xpath('./span[@class="js"]/text()'):
            idiom = li.xpath('./span[@class="hz"]/a/text()')[0]
            interpretation = li.xpath('./span[@class="js"]/text()')[0]
            context[idiom] = interpretation
    func = lambda z: dict([(x, y) for y, x in z.items()])
    idiom_dict = func(func(context))
    return idiom_dict


def run(url, context):
    html = etree.HTML(get_html(url))
    if html.xpath('//a[contains(text(), "末页")]/@href'):
        text = html.xpath('//a[contains(text(), "末页")]/@href')[0]
        letter = re.search('\w', text).group(0) or url.split('/')[-1][0]
        total = re.search('\d+', text).group(0) or 1
    else:
        letter = url.split('/')[-1][0]
        total = 1
    for num in range(1, int(total) + 1):
        page_context = get_curr('http://chengyu.kxue.com/pinyin/' + letter + '_' + str(num) + '.html')
        context.update(page_context)
        print("完成{}的添加,共{}".format(letter + '_' + str(num), total))
    write_data('grandSon/' + url.split('/')[-1][0] + '.json', context)
    print("完成{}的写入".format(url.split('/')[-1][0]))
    return context

def write_data(file, context):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(context, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    url = "http://chengyu.kxue.com/"
    html = etree.HTML(get_html(url))
    file = 'idiom.json'
    context = {}
    urls = html.xpath('//div[@class="content letter"]/li/a/@href')
    for url in urls:
        context.update(run("http://chengyu.kxue.com" + url, {}))
    write_data(file, context)
