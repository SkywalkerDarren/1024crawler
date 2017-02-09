# -*- coding:utf-8  -*-
import re
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import time
import os

PATH = 'D:\\Media\\'  # 存储路径
ROOTURL = 'http://www.t66y.com/'  # 或者1024的代理地址


# url请求
def urlrequest(url):
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
            response = urllib.request.urlopen(request, timeout=5)  #爬取网页超时时间
            test = False
            return response
        except Exception as e:
            print(Exception, ':', e)


#目录地址爬虫，爬取网址
def urlspider(page):
    urldir = ROOTURL + 'thread0806.php?fid=8&search=&type=1&page='
    url = urldir + str(page)
    response = urlrequest(url)
    soup = BeautifulSoup(response.read(), 'html.parser')
    urllist = soup.find_all(href=re.compile('htm_data'), id=re.compile(''))
    length = len(urllist)
    for item in range(length):
        picurl = ROOTURL + urllist[item].attrs['href']

        print(urllist[item].text)
        path = PATH + urllist[item].text + '\\'
        if not os.path.exists(path):
            os.makedirs(path)
        print(picurl)
        picspider(picurl, path)

        if item % 20 == 0:
            time.sleep(3)  #休眠时间


#根据地址下载图片，并编号保存
def download(url, num, path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/55.0.2883.87 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
        'Connection': 'keep-alive',
    }
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request, timeout=60)  #爬取图片超时时间
    img = response
    response.close()
    time.sleep(3)  #休眠时间
    f = open(path + str(num) + '.jpg', 'wb')
    f.write(img.read())
    f.close()


#图片爬虫，爬取地址
def picspider(url, path):
    response = urlrequest(url)
    content = response.read().decode('gbk')
    pattern = re.compile('input src=\'(.*?)\' type=\'image\'', re.S)
    items = re.findall(pattern, content)
    cnt = 0
    for item in items:
        print(item)
        cnt += 1
        download(item, cnt, path)


if __name__ == "__main__":
    for i in range(3):  #爬取页数
        urlspider(i + 1)
