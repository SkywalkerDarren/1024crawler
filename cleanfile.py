# -*-coding:utf-8-*-

import os
PATH = 'D:\\Media\\'

# 清空垃圾文件
cnt = 0
for parent, dirnames, filenames in os.walk(PATH):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for filename in filenames:  # 输出文件信息

        picpath = os.path.join(parent, filename)  # 输出文件路径信息
        if os.path.getsize(picpath) < 10000:
            cnt += 1
            os.remove(picpath)
            print("删除 " + picpath)

print("共删除 " + str(cnt) + " 个文件")

# 清空空文件夹
cnt = 0
for menu in os.listdir(PATH):
    try:
        os.rmdir(PATH + menu)
    except OSError:
        pass
    else:
        print("删除 " + PATH + menu)
        cnt += 1
print("共删除 " + str(cnt) + " 个文件夹")
