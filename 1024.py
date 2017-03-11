# -*- coding:utf-8 -*-
import os
import time
import requests
import re
from bs4 import BeautifulSoup
import threading

PATH = 'D:\\Media\\'  # 存储地址
ROOTURL = 'http://cc.vcly.org/'  # http://www.t66y.com/
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrotestme/55.0.2883.87 Safari/537.36'}


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
            choose = int(input('请输入序号'))
            if 0 < choose < 5:
                return choose
            elif choose == 5:
                return 12
            else:
                print("输入1-5")
        except ValueError:
            print('请输入序号')


# 地址请求
def request(link):
    test = 3
    while test:
        try:
            r = requests.get(link, headers=headers, timeout=30)  # 设置超时
            r.encoding = 'gbk'
            r.raise_for_status()
            time.sleep(1)
            return r
        except requests.ConnectionError:
            print("ConnectionError")
        except requests.HTTPError:
            print("HTTPError")
        except requests.Timeout:
            print("TimeoutError")
        except requests.TooManyRedirects:
            print("TooManyRedirects")
        test -= 1


# 获取网页地址列表
def gethtmllist(choose, maxpage):
    r = request(ROOTURL + 'thread0806.php?fid=8&type=' + str(choose) + '&page=' + str(maxpage))
    soup = BeautifulSoup(r.text, 'html.parser')
    htmlurllist = soup.find_all('a', id="", target="_blank", href=re.compile('htm_data'), title="")
    return htmlurllist


# 获取图片地址列表
def getpiclist(htmlurl):
    r = request(ROOTURL + htmlurl)
    soup = BeautifulSoup(r.text, 'html.parser')
    div = soup.find('div', class_="tpc_content do_not_catch")
    pattern = re.compile('src=\"(.*?)\"')
    picurllist = re.findall(pattern, str(div))
    return picurllist


# 下载图片
def downloadpic(pictureurl, title):
    pic = PATH + title + '\\' + pictureurl.split('/')[-1]
    print(pic)
    print(pictureurl)
    test = 3  # 重试次数
    while test:
        if title.find('!') > 0:  # 排除垃圾文件
            print("rubbish file")
            break
        try:
            if not os.path.exists(PATH + title):
                os.mkdir(PATH + title)
            if not os.path.exists(pic):
                r = request(pictureurl)
                with open(pic, 'wb') as f:
                    f.write(r.content)
                    f.close()
                    print("保存成功 大小为 " + str(len(r.content)//1024) + "KB")
                removebrokenpic(pic)
            else:
                print("文件存在")
                removebrokenpic(pic)
            break
        except FileExistsError:
            print("文件存在错误")
            break
        except OSError:
            print("名称非法")
        except Exception as e:
            print("爬取失败 " + str(e))


def removebrokenpic(picpath):
    if os.path.getsize(picpath) < 10000:  # 删除10KB以下的文件
        os.remove(picpath)
        print("删除失败文件")


if __name__ == "__main__":
    select = userinterface()
    pages = 1
    while True:
        try:
            pages = int(input("爬取页数"))
            break
        except ValueError:
            print("输入正整数")

    for page in range(pages):
        urls = gethtmllist(select, page)
        for url in urls:
            print(url.string)
            html = url.attrs['href']
            print(ROOTURL + html)
            picurls = getpiclist(html)

            # 多线程
            threads = []
            for picurl in picurls:
                # downloadpic(url, title)
                t = threading.Thread(target=downloadpic, args=(picurl, url.string))
                threads.append(t)

            for dl in threads:
                dl.setDaemon(True)
                dl.start()

            for t in threads:
                t.join()

            print("网页完成")

    print("爬取完成")
