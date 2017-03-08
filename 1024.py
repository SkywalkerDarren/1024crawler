#-*- coding:utf-8 -*-
import os
import requests
import re
from bs4 import BeautifulSoup

PATH = 'D:\\Media\\'
ROOTURL = 'http://cc.vcly.org/'
menu = 'thread0806.php?fid=8&type='
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/55.0.2883.87 Safari/537.36'}


def userinterface():
    print("┌────────────────────┐")
    print("│             1024图片爬取器             │")
    print("│             请输入对应序号             │")
    print("│                 1、亚洲                │")
    print("│                 2、欧美                │")
    print("│                 3、动漫                │")
    print("│                 4、写真                │")
    print("│                 5、其他                │")
    print("└────────────────────┘")
    while True:
        try:
            select = int(input('Input an integer: '))
            if 0 < select < 5:
                return select
            elif select == 5:
                return 12
            else:
                print("输入1-5")
        except ValueError:
            print('请输入序号')


def request(url):
    try:
        r = requests.get(ROOTURL + url, headers=headers)
        r.encoding = 'gbk'
        print(r.status_code)
        r.raise_for_status()
        return r
    except ConnectionError:
        print("ConnectionError")


def gethtmllist():
    select = userinterface()
    r = request(menu + str(select))
    soup = BeautifulSoup(r.text, 'html.parser')

    for url in soup.find_all('a', id="", target="_blank", href=re.compile('htm_data'), title=""):
        print(url.string)
        html = url.attrs['href']
        print(ROOTURL + html)
        getpiclist(html, url.string)


def getpiclist(html, title):
    r = request(html)
    soup = BeautifulSoup(r.text, 'html.parser')

    div = soup.find('div', class_="tpc_content do_not_catch")
    pattern = re.compile('src=\"(.*?)\"')
    items = re.findall(pattern, str(div))
    for url in items:
        downloadpic(url, title)


def downloadpic(url, title):
    pic = PATH + title + '\\' + url.split('/')[-1]
    print(pic)
    print(url)

    try:
        if not os.path.exists(PATH + title):
            os.mkdir(PATH + title)
        if not os.path.exists(pic):
            r = requests.get(url)
            with open(pic, 'wb') as f:
                f.write(r.content)
                f.close()
                print("保存成功")
        else:
            print("文件存在")
    except:
        print("爬取失败")


if __name__ == "__main__":
    gethtmllist()
