# -*-coding:utf-8-*-

import time
import os
import requests
from cleanfile import removebrokenpic
from bs4 import BeautifulSoup
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrotestme/55.0.2883.87 Safari/537.36'}


# 地址请求
def request(url):
    test = 3
    while test:
        try:
            r = requests.get(url, headers=headers, timeout=30)  # 设置超时
            r.encoding = 'gbk'
            r.raise_for_status()
            time.sleep(0.1)
            return r
        except requests.Timeout as e:
            print("Timeout " + str(e))
        except requests.ConnectionError as e:
            print("ConnectionError " + str(e))
        except Exception as e:
            print("错误原因 " + str(e))
            break
        test -= 1
    return 0


# 获取网页地址列表
def gethtmllist(rooturl, choose, maxpage):
    r = request(rooturl + 'thread0806.php?fid=8&type=' + str(choose) + '&page=' + str(maxpage))
    soup = BeautifulSoup(r.text, 'html.parser')
    string = 'htm_data'
    htmlurllist = soup.find_all('a', id="", target="_blank", href=re.compile(string), title="")
    return htmlurllist


# 获取图片地址列表
def getpiclist(rooturl, htmlurl):
    r = request(rooturl + htmlurl)
    soup = BeautifulSoup(r.text, 'html.parser')
    div = soup.find('div', class_="tpc_content do_not_catch")
    string = 'src=\"(.*?)\"'
    pattern = re.compile(string)
    picurllist = re.findall(pattern, str(div))
    return picurllist


# 下载图片
def downloadpic(path, pictureurl, title):
    strings = pictureurl.split('/')[-1].replace("&amp;", ".").replace("image.php?id=", "")
    pic = path + title + '\\' + strings
    try:
        if not os.path.exists(path + title):
            os.mkdir(path + title)
        if not os.path.exists(pic):
            r = request(pictureurl)
            with open(pic, 'wb') as f:
                f.write(r.content)
                f.close()
                print("保存成功 大小为 " + str(len(r.content)//1024) + "KB")
            removebrokenpic(pic)
        else:
            removebrokenpic(pic)
    except:
        print("爬取失败 " + pictureurl)
