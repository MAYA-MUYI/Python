import requests
from bs4 import BeautifulSoup
import urllib.request
from PIL import Image
import pytesseract
import re
import os

URL = 'http://www.heibanke.com/lesson/crawler_ex04/'
LOGIN_URL = 'http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex04/'

login_page = requests.get(LOGIN_URL)

login_data = {
    'csrfmiddlewaretoken': login_page.cookies['csrftoken'],
    'username': 'fuyufjh',
    'password': '142857',
}

login_res = requests.post(LOGIN_URL, data=login_data, cookies=login_page.cookies, allow_redirects=False)

number = 0

while True:
    prob_res = requests.get(URL, cookies=login_res.cookies)
    soup = BeautifulSoup(prob_res.text, 'lxml')
    captcha_id = soup.find(id='id_captcha_0')['value']
    captcha_image_url = 'http://www.heibanke.com' + soup.find(alt='captcha')['src']
    try:
        urllib.request.urlretrieve(captcha_image_url, 'captcha.png')
        vcode_img = Image.open('captcha.png')
        vcode = pytesseract.image_to_string(vcode_img, lang='eng')
    finally:
        os.remove('captcha.png')
    if not re.match(r'[A-Z]{4}$', vcode):
        print('recognizing failed')
        continue
    data = {
        'username': 'fuyufjh',
        'password': number,
        'captcha_0': captcha_id,
        'captcha_1': vcode,
        'csrfmiddlewaretoken': prob_res.cookies['csrftoken']
    }

    print(data)
    guess_res = requests.post(URL, data=data, cookies=login_res.cookies)

    if '验证码输入错误' in guess_res.text:
        print('verify code error')
        continue
    elif '密码错误' in guess_res.text:
        print('Password is not %d' % number)
        number += 1
    else:
        print('Password is %d' % number)
        break