#-*- coding:utf-8  -*-
import re
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import time

def Urlreq(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
        'Connection': 'keep-alive',
    }
    test = True
    while test:
        try:
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request, timeout=3)
            test = False
            return response
        except:
            print("timeout")



def Urlspider(page):
    urldir = 'http://sbl8.xyz/thread0806.php?fid=8&search=&type=1&page='
    url = urldir + str(page)
    response = Urlreq(url)
    soup = BeautifulSoup(response.read(), 'html.parser')
    urllist = soup.find_all(href=re.compile('htm_data'), id=re.compile(''))
    length = len(urllist)
    for item in range(length):
        urlin = 'http://sbl8.xyz/' + urllist[item].attrs['href']
        print(urlin)
        Picspider(urlin)
        if item % 20 == 0:
            time.sleep(3)
        print(urllist[item].text)


def Download(url, num):
    f = Urlreq(url)



def Picspider(url):
    for test in range(3):
        response = Urlreq(url)
        if response != 0:
            content = response.read().decode('gbk')
            pattern = re.compile('input src=\'(.*?)\' type=\'image\'', re.S)
            items = re.findall(pattern, content)
            for item in items:
                print(item)
            break

if __name__ == "__main__":
    for i in range(3):
        Urlspider(i + 1)