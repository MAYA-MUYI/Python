#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@software: Pycharm
@file: mark.py
@time: 2019/7/30 10:25
@desc:
'''

from lxml import etree

def getData(table):
    html = etree.HTML(table)
    body = []
    trs = html.xpath('//table//tr')
    #获取表头
    title = [th.xpath('./text()')[0] for th in trs[0]]
    #根据表头长度确定符号线
    line = ["----"] * len(title)
    #获取表格内容并用嵌套的列表保存
    for td in trs[1:]:
        if td.xpath('./td/code'):
            body.append([
                td.xpath('./td/text()')[0],
                td.xpath('./td/text()')[1],
                td.xpath('./td//text()')[2] + td.xpath('./td/text()')[2]
            ])
        else:
            body.append([
                td.xpath('./td/text()')[0],
                td.xpath('./td/text()')[1],
                td.xpath('./td//text()')[2]
            ])
    return title, line, body


def printData(table):
    title, line, body = getData(table)
    # 用"|"分隔获取到的数据并依次打印
    result = [" | ".join(data) for data in body]
    print("| " + "| ".join(title) + "|")
    print("| " + " | ".join(line) + "|")
    for data in result:
        print("| " + data + "|")


def writeData(table):
    title, line, body = getData(table)
    result = [" | ".join(data) for data in body]
    with open("table.md", 'w', encoding='utf-8') as f:
        f.write("| " + "| ".join(title) + "|" + "\n")
        f.write("| " + " | ".join(line) + "|" + "\n")
        for data in result:
            f.write("| " + data + "|" + "\n")

if __name__ == '__main__':
    table = '''
        <table>
<thead>
<tr>
<th>运算符</th>
<th>说明</th>
<th>举例</th>
</tr>
</thead>
<tbody>
<tr>
<td>+</td>
<td>加法</td>
<td><code>expr $x + $y</code> 结果为 30。</td>
</tr>
<tr>
<td>-</td>
<td>减法</td>
<td><code>expr $x - $y</code> 结果为 -10。</td>
</tr>
<tr>
<td>*</td>
<td>乘法</td>
<td><code>expr $x * $y</code> 结果为 200。</td>
</tr>
<tr>
<td>/</td>
<td>除法</td>
<td><code>expr $y / $x</code> 结果为 2。</td>
</tr>
<tr>
<td>%</td>
<td>取余</td>
<td><code>expr $y % $x</code> 结果为 0。</td>
</tr>
<tr>
<td>=</td>
<td>赋值</td>
<td><code>x=$y</code> 将把变量 y 的值赋给 x。</td>
</tr>
<tr>
<td>==</td>
<td>相等。用于比较两个数字，相同则返回 true。</td>
<td><code>[ $x == $y ]</code> 返回 false。</td>
</tr>
<tr>
<td>!=</td>
<td>不相等。用于比较两个数字，不相同则返回 true。</td>
<td><code>[ $x != $y ]</code> 返回 true。</td>
</tr>
</tbody>
</table>
    '''
    printData(table)
    # writeData(table)
