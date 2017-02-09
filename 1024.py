# -*- coding:utf-8  -*-
import re
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import time
import os


PATH = 'D:\\Media\\'
ROOTURL = 'http://www.t66y.com/'


def urlRequest(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/55.0.2883.87 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
        'Connection': 'keep-alive',
    }
    test = True
    while test:
        try:
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request, timeout=5)
            test = False
            return response
        except Exception as e:
            print(Exception, ':', e)


def urlSpider(page):
    urlDir = ROOTURL + 'thread0806.php?fid=8&search=&type=1&page='
    url = urlDir + str(page)
    response = urlRequest(url)
    soup = BeautifulSoup(response.read(), 'html.parser')
    urlList = soup.find_all(href=re.compile('htm_data'), id=re.compile(''))
    length = len(urlList)
    for item in range(length):
        picUrl = ROOTURL + urlList[item].attrs['href']

        print(urlList[item].text)
        path = PATH + urlList[item].text + '\\'
        try:
            os.makedirs(path)
        except:
            pass
        print(picUrl)
        picSpider(picUrl, path)

        if item % 20 == 0:
            time.sleep(3)


def download(url, num, path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/55.0.2883.87 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
        'Connection': 'keep-alive',
    }
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request, timeout=60)
    img = response
    response.close()
    time.sleep(3)
    f = open(path + str(num) + '.jpg', 'wb')
    f.write(img.read())
    f.close()


def picSpider(url, path):
    response = urlRequest(url)
    content = response.read().decode('gbk')
    pattern = re.compile('input src=\'(.*?)\' type=\'image\'', re.S)
    items = re.findall(pattern, content)
    cnt = 0
    for item in items:
        print(item)
        cnt = cnt + 1
        download(item, cnt, path)


if __name__ == "__main__":
    for i in range(3):
        urlSpider(i + 1)
