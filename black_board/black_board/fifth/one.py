import re
import requests
from lxml import etree
import pytesseract
from PIL import Image,ImageEnhance

def verification_Code(img_url):
    #保存验证码

    imgs = requests.get(img_url).content
    with open('1.jpg', 'wb') as f:
        f.write(imgs)

    image = Image.open('1.jpg')
    imgry = image.convert('L')#图像加强，二值化
    sharpness = ImageEnhance.Contrast(imgry)#对比度增强
    sharp_img = sharpness.enhance(2.0)
    sharp_img.save('1.jpg')

    text = pytesseract.image_to_string(image)
    return text



def login():
    login_url = "http://www.heibanke.com/accounts/login"
    session = requests.Session()
    token = session.get(login_url).cookies['csrftoken']
    data = {
        'username': 'Koelre',
        'password': 'lixue961314',
        'csrfmiddlewaretoken': token
    }
    session.post(login_url, data)
    print("登录成功")
    return session

def ex05(a=1,password=1):
    url = "http://www.heibanke.com/lesson/crawler_ex04/"
    session = login()
    html = session.get(url).text
    etr = etree.HTML(html)
    token = etr.xpath('/html/body/div/div/div[2]/form/input/@value')[0].strip()
    img_src = etr.xpath('/html/body/div/div/div[2]/form/div[3]/img/@src')[0].strip()
    #验证码连接
    img_url = 'http://www.heibanke.com' + str(img_src)
    #图片code
    pic_code = etr.xpath('//*[@id="id_captcha_0"]/@value')[0]
    text = verification_Code(img_url)

    data = {
        "csrfmiddlewaretoken": token,
        "username": "a",
        "password": password,
        "captcha_0": pic_code,
        "captcha_1": text
    }

    res = session.post(url, data).text
    verification_result = re.findall("验证码输入错误", res)
    passwd_result = re.findall('您输入的密码错误', res)
    h3 = re.findall('<h3>(.*?)</h3>', res)
    if verification_result:
        print(h3)
        print(text)
        print("重试")
        ex05(a+1, password)
    else:
        if passwd_result:
            print(h3)
            print("密码：%s错误" %password)
            ex05(a, password+1)
        else:
            print("闯关成功，密码是：%s" %password)
            print(h3)



if __name__ == '__main__':
    ex05()