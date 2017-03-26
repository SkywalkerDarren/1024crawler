# -*-coding:utf-8-*-

import threading
from crawler import *
from cleanfile import cleanfile
from cleanfile import repeatfile

PATH = 'D:\\Media\\'  # 存储地址
ROOTURL = 'http://c6.3hx.info/'  # http://www.t66y.com/的代理地址


def testrooturl(rooturl):
    try:
        r = requests.get(rooturl)
        r.raise_for_status()
    except Exception as e:
        print("地址已失效，请更换 " + str(e))
        exit()


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
    print("文件将保存在" + PATH)
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


# 多线程爬虫
def threadspyder():
    threads = []
    for picurl in picurls:
        t = threading.Thread(target=downloadpic, args=(PATH, picurl, url.string))
        threads.append(t)
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    print("网页完成")


if __name__ == "__main__":
    testrooturl(ROOTURL)
    select = userinterface()
    start = 1
    end = 2
    while True:
        try:
            start = int(input("起始页数"))
            end = int(input("结束页数")) + 1
            break
        except ValueError:
            print("输入正整数")
    for page in range(start, end):
        urls = gethtmllist(ROOTURL, select, page)
        for url in urls:
            print(url.string)
            if url.string.find('!') > 0 or url.string.find('！') > 0 or url.string.find('~') > 0:  # 排除垃圾文件
                print("垃圾网页")
                continue
            html = url.attrs['href']
            print(ROOTURL + html)
            picurls = getpiclist(ROOTURL, html)
            threadspyder()
        print("---------------------第 " + str(page) + " 页完成---------------------")
    print("爬取完成")
    print("进行文件清理")
    cleanfile(PATH)
    print('列出重复文件')  # 自行选择是否清理
    repeatfile(PATH)
    print('清理结束')
