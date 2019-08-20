#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@software: Pycharm
@file: query.py
@time: 2019/8/15 14:09
@desc:
'''
import argparse
import json
import random


def get_data(file):
    with open(file,  'r', encoding='utf-8') as f:
        idioms = json.load(f)
    return idioms


def idiom_type(idiom):
    if idiom[0] == idiom[1] and idiom[2] == idiom[3] and idiom[1] != idiom[2]:
        return "AABB"
    elif idiom[0] != idiom[1] and idiom[0] != idiom[2] and idiom[1] != idiom[2] and idiom[2] == idiom[3]:
        return "ABCC"
    elif idiom[0] == idiom[1] and idiom[2] != idiom[3] and idiom[1] != idiom[2]:
        return "AABC"
    elif idiom[0] != idiom[1] and idiom[0] == idiom[2] and idiom[0] != idiom[3] and idiom[1] != idiom[3]:
        return "ABAC"
    elif idiom[0] == idiom[3] and idiom[0] != idiom[1] and idiom[0] != idiom[2] and idiom[1] != idiom[2]:
        return "ABCA"
    elif idiom[0] != idiom[1] and idiom[0] != idiom[3] and idiom[1] != idiom[3] and idiom[1] == idiom[2]:
        return "ABBC"
    elif idiom[0] != idiom[1] and idiom[0] != idiom[2] and idiom[1] == idiom[3] and idiom[1] != idiom[2]:
        return "ABCB"
    else:
        return "other"


def next_idiom(idiom, idioms, tmp):
    idioms = idioms.keys()
    for data in idioms:
        if data[0] == idiom[-1]:
            tmp.append(data)
    return random.choice(tmp) if tmp else None


def game(file, key=None):
    key = key if key else input_or_default_key('安之若素', 'please the first idiom\n')
    print(key)
    while next_idiom(key, get_data(file), []):
        key = next_idiom(key, get_data(file), [])
        print(key)


def search_by_key(key, idioms, context):
    for k, v in idioms.items():
        if key in k or key in v:
            context[k] = v
    return context


def search_by_type(type, idioms, context):
    for k, v in idioms.items():
        if len(k) == 4 and idiom_type(k) == type:
            context[k] = v
    return context


def result_by_type(type, args, file, length=-1):
    type_result = search_by_type(type, get_data(file), {})
    if length != -1:
        args.length = length
    if len(type_result) > args.length:
        keys = []
        print("*************************************")
        print("****成语 ：释义**********************")
        for index, key in enumerate(type_result):
            if index < args.length:
                keys.append(key)
        for k, v in type_result.items():
            if k in keys:
                print(k + " : " + v)
    else:
        if len(type_result) == 0:
            print("未找到相关项")
        else:
            print("*************************************")
            print("****成语 ：释义**********************")
            for k, v in type_result.items():
                print(k + " : " + v)


def search_by_key_type(key, type, idioms, context, keys):
    for k, v in idioms.items():
        if key in k or key in v:
            keys.append(k)
    for k, v in idioms.items():
        if k in keys and len(k) == 4 and idiom_type(k) == type:
            context[k] = v
    return context


def result_by_key_type(key, type, args, file, length=-1):
    result = search_by_key_type(key, type, get_data(file), {}, [])
    if length != -1:
        args.length = length
    if len(result) > args.length:
        keys = []
        print("*************************************")
        print("****成语 ：释义**********************")
        for index, key in enumerate(result):
            if index < args.length:
                keys.append(key)
        for k, v in result.items():
            if k in keys:
                print(k + " : " + v)
    else:
        if len(result) == 0:
            print("未找到相关项")
        else:
            print("*************************************")
            print("****成语 ：释义**********************")
            for k, v in result.items():
                print(k + " : " + v)


def result_by_key(key, args, file, length=-1):
    key_result = search_by_key(key, get_data(file), {})
    if length != -1:
        args.length = length
    if len(key_result) > args.length:
        keys = []
        print("*************************************")
        print("****成语 ：释义**********************")
        for index, key in enumerate(key_result):
            if index < args.length:
                keys.append(key)
        for k, v in key_result.items():
            if k in keys:
                print(k + " : " + v)
    else:
        if len(key_result) == 0:
            print("未找到相关项")
        else:
            print("*************************************")
            print("****成语 ：释义**********************")
            for k, v in key_result.items():
                print(k + " : " + v)


def input_or_default_num(default, hint):
    data = input(hint)
    if data.isdigit():
        return eval(data)
    else:
        return default


def input_or_default_key(default, hint):
    key = input(hint)
    if key:
        return key
    else:
        return default

def input_or_default_type(default, hint):
    types = ['AABB', 'ABCC', 'AABC', 'ABAC', 'ABCA', 'ABBC', 'ABCB']
    type = input(hint)
    if type in types:
        return type
    else:
        return default


def search_by_interaction(args, file):
    print("*************************************")
    print("1)      By Type      ****************")
    print("2)      By Key_Word  ****************")
    print("3)      By Key_Word & Type **********")
    print("4)      Game ************************")
    print("5)      Exit  ***********************")
    print("*************************************")
    num = input_or_default_num(1, "****please input search method(Default: By Type)**************\n")
    if num == 2:
        key = input_or_default_key("安", "please your key(Default: 安)\n")
        length = input_or_default_num(10, "please the number of idioms(Default：10)\n")
        result_by_key(key, args, file, length)
    elif num == 3:
        key = input_or_default_key("安", "please your key(Default: 安)\n")
        type = input_or_default_type("AABB", "please your type(Default：AABB)\n")
        length = input_or_default_num(10, "please the number of idioms(Default：10)\n")
        result_by_key_type(key, type, args, file, length)
    elif num == 4:
        game(file)
    elif num == 5:
        exit()
    else:
        print("**************      Type     ****************************")
        print("**************      AABB   ：平平安安    ****************")
        print("**************      ABCC   ：喜气洋洋    ****************")
        print("**************      AABC   ：鼎鼎大名    ****************")
        print("**************      ABAC   ：不声不响    ****************")
        print("**************      ABCA   ：贼喊捉贼    ****************")
        print("**************      ABBC   ：自欺欺人    ****************")
        print("**************      ABCB   ：爱理不理    ****************")
        print("*********************************************************")
        type = input_or_default_type("AABB", "please your type(Default：AABB)\n")
        length = input_or_default_num(10, "please the number of idioms(Default：10)\n")
        result_by_type(type, args, file, length)


def search(file):
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", type=str, choices=["AABB", "ABCC", "AABC", "ABAC", "ABCA",
                                                           "ABBC", "ABCB", "ABCC"],
                        help="search the idiom by type")
    parser.add_argument("-i", "--interaction", help="enter the type of interaction",
                        action="store_true")
    parser.add_argument("-k", "--key", type=str, help="search idiom by key word",)
    parser.add_argument("-l", "--length", type=int, default=30,
                        help="search the idiom by type")
    parser.add_argument("-g", "--game", type=str,
                        help="enter the game")

    args = parser.parse_args()
    if args.type and not args.key:
        result_by_type(args.type, args, file)
    elif args.key and not args.type:
        result_by_key(args.key, args, file)
    elif args.key and args.type:
        result_by_key_type(args.key, args.type, args, file)
    elif args.interaction and not args.type and not args.key:
        search_by_interaction(args, file)
    elif args.game and not args.type and not args.key and not args.interaction:
        game(file, args.game)
    else:
        parser.print_help()


if __name__ == '__main__':
    search('idiom.json')
