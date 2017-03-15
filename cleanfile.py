# -*-coding:utf-8-*-

import os
import hashlib
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
                print("删除 " + picpath)
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


def chkmd5(filepath):
    with open(filepath, 'rb') as f:
        m = hashlib.md5(f.read())
        f.close()
        return m.hexdigest()


def filemd5(path):
    filedic = {}
    for parent, dirnames, filenames in os.walk(path, False):
        for filename in filenames:
            filepath = os.path.join(parent, filename)
            md5 = chkmd5(filepath)
            filedic.setdefault(md5, []).append(filepath)
    return filedic


def repeatfile(path):
    print('正在清理重复文件，可能需要几分钟')
    fdic = filemd5(path)
    with open(PATH + '重复文件.txt', 'w', encoding='utf-8') as f:
        for i in fdic.keys():
            if len(fdic[i]) > 1:
                f.write(str(fdic[i]).replace("\', \'", " ").replace("[\'", "")
                        .replace("\']", "").replace("\\\\", "\\") + '\n')
        f.close()


if __name__ == "__main__":
    print("开始清理")
    cleanfile(PATH)
    x = input('是否列出重复文件(y/n):')
    if x == 'y' or x == 'Y':
        repeatfile(PATH)
    print('清理结束')
