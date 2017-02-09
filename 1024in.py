#-*- coding:utf-8  -*-
import re
import urllib.request

url = 'http://sbl8.xyz/htm_data/8/1702/2248701.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
    'Connection': 'keep-alive'
}

request = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(request)
content = response.read().decode('gbk')
pattern = re.compile('input src=\'(.*?)\' type=\'image\'', re.S)
items = re.findall(pattern, content)
for item in items:
    print (item)
