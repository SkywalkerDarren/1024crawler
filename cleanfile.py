# -*-coding:utf-8-*-

import os
PATH = 'D:\\Media\\'  # 存储地址


# 清空垃圾文件
def cleanfile(path):
    i = 0
    j = 0
    for parent, dirnames, filenames in os.walk(path, False):  # 遍历文件
        for filename in filenames:
            picpath = os.path.join(parent, filename)  # 输出文件路径信息
            if os.path.getsize(picpath) < 10000:
                i += 1
                print("删除 " + picpath + " " + str(os.path.getsize(picpath)))
                os.remove(picpath)
        for dirname in dirnames:
            try:
                os.rmdir(path + dirname)
            except OSError:
                pass
            else:
                j += 1
                print("删除 " + path + dirname)
    print("共删除 " + str(i) + " 个文件")
    print("共删除 " + str(j) + " 个文件夹")


def removebrokenpic(path):
    if os.path.getsize(path) < 10000:  # 删除10KB以下的文件
        os.remove(path)
        print("删除失败文件")

if __name__ == "__main__":
    cleanfile(PATH)
