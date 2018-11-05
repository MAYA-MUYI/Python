# _*_ coding:utf-8 _*_

import json
def main():
    f = open("poker.json", "r", encoding='utf-8')
    newarr = {}
    dic = json.loads(f.read())
    for i in range(65, 91):
        arr = []
        for line in dic:
            if str(line["title"])[0].upper() == chr(i):
                arr.append(line)
        newarr[chr(i)] = arr
    print(newarr)


if __name__ == '__main__':
    main()
