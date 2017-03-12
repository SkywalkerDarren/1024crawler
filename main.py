# -*- coding:utf-8 -*-

import threading
from spider import *
from cleanfile import cleanfile

PATH = 'D:\\Media\\'  # 存储地址
ROOTURL = 'http://www.t66y.com/'  # http://www.t66y.com/


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


if __name__ == "__main__":
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
            if url.string.find('!') > 0:  # 排除垃圾文件
                print("垃圾网页")
                continue
            html = url.attrs['href']
            print(ROOTURL + html)
            picurls = getpiclist(ROOTURL, html)

            # 多线程
            threads = []
            for picurl in picurls:
                t = threading.Thread(target=downloadpic, args=(PATH, picurl, url.string))
                threads.append(t)
            for dl in threads:
                dl.setDaemon(True)
                dl.start()
            for t in threads:
                t.join()
            print("网页完成")
        print("---------------------第 " + str(page) + " 页完成---------------------")

    print("爬取完成")

    print("进行文件清理")
    cleanfile(PATH)
