#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@software: Pycharm
@file: money.py
@time: 2019/10/30 17:42
@desc:
'''
import re


class Money2Word(object):

    def __init__(self, num):
        """
        :param num: 用户传入的数字
        初始化参数，包括：
        {
            check_num ：int/float    用作检查输入的数字
            num：str    用作转换的阿拉伯数字字符串，排除`.00`的情况
            trans_tab：dict    字符映射转换表
            dec_label：list    小数部分的单位列表
            int_label：list    整数部分的单位列表
            int_string：str    整数部分构成的字符串
            dec_string：str    小数部分构成的字符串
        }
        """
        # 去除00的情况
        self.check_num = num
        self.num = str(num).rstrip('.0')
        self.trans_tab = str.maketrans('0123456789', '零壹贰叁肆伍陆柒捌玖')
        self.dec_label = ['角', '分']
        self.int_label = ['', '拾', '佰', '仟', '万', '拾', '佰', '千', '亿', '拾', '百', '千', '兆']
        self.int_string = ''
        self.dec_string = ''

    def data_checker(self):
        """
        判断用户传入的数据是否为数字类型且长度适中，最大仅支持到兆位，小数点后两位
        :return: 数据无误则返回True，否则False
        """
        if not isinstance(self.check_num, (int, float)):
            return False
        elif isinstance(self.check_num, int) and len(self.num) > 13:
            return False
        elif isinstance(self.check_num, float):
            int_part, dec_part = str(self.check_num).split('.')
            if len(int_part) > 13 or len(dec_part) > 2:
                return False
        return True

    def number2word(self):
        if self.data_checker():
            # 判断是否是纯整数或者带小数
            if len(self.num.split('.')) == 2:
                # 分离整数部分和小数部分
                int_part, dec_part = self.num.translate(self.trans_tab).split('.')
                # 对小数部分进行处理
                if len(dec_part) == 2:
                    self.dec_string = ''.join([
                        dec_part[i] + self.dec_label[i] for i in range(len(dec_part))
                    ]).replace('零角', '零')

                else:
                    self.dec_string = ''.join([
                        dec_part[i] + self.dec_label[i] for i in range(len(dec_part))
                    ])
                # 处理整数部分
                int_part = list(reversed(int_part))
                int_list = list(reversed([
                    int_part[i] + self.int_label[i] if int_part[i] != '零' else '零' for i in range(len(int_part))
                ]))
                if int_list[-1] == '零':
                    self.int_string = re.sub(r'零{2,}', '零', ''.join(int_list)).rstrip('零') + '圆零'
                else:
                    self.int_string = re.sub(r'零{2,}', '零', ''.join(int_list)).rstrip('零') + '圆'
                print(self.int_string + self.dec_string)
            else:
                # 纯整数的情况则仅处理整数部分
                int_part = list(reversed(self.num.translate(self.trans_tab)))
                int_list = list(reversed([
                    int_part[i] + self.int_label[i] if int_part[i] != '零' else '零' for i in range(len(int_part))
                ]))
                if int_list[-1] == '零':
                    self.int_string = re.sub(r'零{2,}', '零', ''.join(int_list)).rstrip('零') + '圆零'
                else:
                    self.int_string = re.sub(r'零{2,}', '零', ''.join(int_list)).rstrip('零') + '圆'
                print(self.int_string + self.dec_string)
        else:
            print("请输入正确的金额")


class Word2Money(object):
    def __init__(self, word):
        """
        :param word: 用户传入的中文字符串
        初始化参数，包括：
        {
            is_int ：int/float    是否为纯整数
            word：str    用作转换的中文金额
            int_part：str    整数部分字符串
            dec_part：str    小数部分字符串
            int_level：list    整数部分的单位列表
            trans_tab：dict    映射表
            pattern：_sre.SRE_Pattern    正则表达式compile规则
        }
        """
        if word.endswith('圆'):
            self.int_part = word
            self.is_int = True
        elif word.endswith('角') or word.endswith('分'):
            self.int_part = word[:word.index('圆') + 1]
            self.dec_part = word[word.index('圆') + 1:]
            self.is_int = False
        self.word = word
        self.int_level = [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000, 10000000000,
                           100000000000, 1000000000000]
        self.trans_tab = str.maketrans('零壹贰叁肆伍陆柒捌玖', '0123456789')
        self.pattern = re.compile('(?:(.*?)兆)?(?:(.*?)千)?(?:(.*?)百)?(?:(.*?)拾)?(?:(.*?)亿)?(?:(.*?)千)?(?:(.*?)佰)'
                                  '?(?:(.*?)拾)?(?:(.*?)万)?(?:(.*?)仟)?(?:(.*?)佰)?(?:(.*?)拾)?(.*?)圆')

    def data_check(self):
        """
        数据检查，是否符合输入要求
        :return: 传入的数据不是字符串类型或者长度越界则返回False，否则返回True
        """
        if not isinstance(self.word, str):
            return False
        if self.is_int:
            if len(self.int_part) > 26:
                return False
            else:
                return True
        else:
            if len(self.int_part) > 26 or len(self.dec_part) > 4:
                return False
            else:
                return True

    def word_format(self, word):
        """

        :param word: 对传入的word字符串进行映射处理
        :return: 根据传入字符串的长度进行处理后执行映射
        """
        if len(word) > 1:
            return word[-1].translate(self.trans_tab)
        elif len(word) == 0:
            return '零'.translate(self.trans_tab)
        return word.translate(self.trans_tab)

    def word2number(self):
        if self.data_check():
            # 处理纯整数
            if self.is_int:
                # 用正则表达式按照模板检索（从兆位到个位，没有对应项则为空）
                word_list = re.findall(self.pattern, self.int_part)[0]
                # 按照映射表执行映射后组合成数字列表
                number_list = list(reversed(list(map(self.word_format, word_list))))
                # 将数字列表与数字单位列表的对应索引项进行相乘后求和
                print(sum(
                    [int(number_list[i]) * self.int_level[i] for i in range(len(number_list))]
                ))
            else:
                # 整数部分
                int_word_list = re.findall(self.pattern, self.int_part)[0]
                int_number_list = list(reversed(list(map(self.word_format, int_word_list))))
                int_number = sum(
                    [int(int_number_list[i]) * self.int_level[i] for i in range(len(int_number_list))]
                )
                # 处理小数部分，根据长度分别处理
                if len(self.dec_part) == 4:
                    dec_word_list = list(self.dec_part[0] + self.dec_part[2])
                    dec_number_list = list(map(self.word_format, dec_word_list))
                    dec_number = int(dec_number_list[0]) * 0.1 + int(dec_number_list[1]) * 0.01

                elif len(self.dec_part) == 3:
                    dec_number = int(self.word_format(self.dec_part[:-1])) * 0.01
                else:
                    dec_number = int(self.word_format(self.dec_part[:-1])) * 0.1
                print(int_number + dec_number)
        else:
            print("请输入正确的金额")



if __name__ == '__main__':
    # Money2Word(9999999999999.19).number2word()
    # Money2Word(9029999.01).number2word()
    # Money2Word(129999909).number2word()
    Word2Money('玖兆玖千玖百玖拾玖亿玖千玖佰玖拾玖万玖仟玖佰玖拾玖圆壹角').word2number()
    Word2Money('玖兆玖千玖百玖拾玖亿玖千玖佰玖拾玖万玖仟玖佰玖拾玖圆零玖分').word2number()
    Word2Money('壹亿贰千玖佰玖拾玖万玖仟玖佰零玖圆').word2number()
