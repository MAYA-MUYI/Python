"""
黑板客爬虫闯关第五关
http://www.heibanke.com/lesson/crawler_ex04
验证码处理
answer is 22
"""

import Image

from PIL import Image
from io import BytesIO
import pytesseract
import bs4
from bs4 import BeautifulSoup
import requests
import os
import re

pytesseract.pytesseract.tesseract_cmd = "D:\\Program Files (x86)\\Tesseract-OCR\\tesseract"

url = "http://www.heibanke.com/lesson/crawler_ex04/"
login_url = "http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex04/"

data={'username': 'medyg', 'password': '19931122bihu', 'csrfmiddlewaretoken': ''}

""" 打开登陆页面 """
loginr = requests.get(login_url)
if loginr.status_code == 200:
    cookie = loginr.cookies
    print("get login_url success, csrftoken is :" + cookie['csrftoken'])
else:
    print("get login_url failed")
data['csrfmiddlewaretoken'] = cookie['csrftoken']

""" 登陆 """
signinr = requests.post(login_url, data = data, allow_redirects = False, cookies = cookie)
if signinr.status_code == 302:
    cookie2 = signinr.cookies
    print("post login_url success, csrftoken is :" + cookie2['csrftoken'])
else:
    print("post login_url failed, status_code is " + str(signinr.status_code))

data['csrfmiddlewaretoken'] = cookie2['csrftoken']
""" 获取并识别验证码（Using Tesseract-Ocr） """
guesses = 0
guess_success = 0
def get_captcha():
    global guesses
    print("\n开始获取第%d次验证码" % guesses)
    captchar = requests.get(url, cookies = cookie2)
    soup = BeautifulSoup(captchar.text, "lxml")
    img_src = soup.find('img', class_='captcha').get('src')
    img_url = "http://www.heibanke.com" + img_src
    captcha_0_value = soup.find('input', id="id_captcha_0").get('value')
    data['captcha_0'] = captcha_0_value

    imgr = requests.get(img_url)
    if imgr.status_code == 200:
        print("验证码图片获取成功")
        captcha_img = Image.open(BytesIO(imgr.content)) # content 是bytes类型
    else:
        print("验证码图片获取失败，重新获取")
        return get_captcha()
    #captcha_img.show()
    print("正在识别……")
    captcha_1 = pytesseract.image_to_string(captcha_img) # 使用tesseract进行验证码识别
    captcha_1 = captcha_1.strip()
    captcha_1 = captcha_1.replace(' ', '')
    guesses += 1
    if not re.match('^[A-Z | a-z]{4}$', captcha_1):
        print("验证码识别失败：" + captcha_1)
        return get_captcha()
    else:
        print("验证码识别成功：" + captcha_1)
        return captcha_0_value, captcha_1
""" 猜密码 """
pw = 0
while True:
    captcha_0_value, captcha_1 = get_captcha()
    guess_data = {
        'username' : 'medyg',
        'password' : pw,
        'csrfmiddlewaretoken' : cookie2['csrftoken'],
        'captcha_0' : captcha_0_value,
        'captcha_1' : captcha_1
    }
    print(guess_data)
    guessr = requests.post(url, guess_data, cookies = cookie2)
    if guessr.status_code == 200:
        soup = BeautifulSoup(guessr.text, 'lxml')
        h3 = soup.find('h3')
        if '验证码输入错误' in h3.text:
            print("验证码错误，重新输入验证码，验证码识别率为%f" % (float(guess_success) / guesses))
        elif '密码错误' in h3.text:
            guess_success += 1
            print("密码错误，重新输入密码，验证码识别率为%f" % (float(guess_success) / guesses))
            pw += 1
        else:
            guess_success += 1
            print(h3.text)
            print("密码是%d，验证码识别率为%f" % (pw,  (float(guess_success) / guesses)))
            break
    else:
        print("请求失败，重新请求%d" % guessr.status_code)