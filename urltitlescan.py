import requests
import lxml.html
import time
import sys
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
import os


urlalive = []
urldead =[]
dirlist = []
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0','Connection':'close'}

def get_url(file):
    with open(file,'r') as f:
        list = f.readlines()
    for url in list:
        url = url.strip()
        if ('http' or 'https') in url:
            try:
                requests.get(url,timeout=0.1,headers=headers)
                urlalive.append(url)
            except requests.exceptions.ConnectTimeout:
                urldead.append(url)
            except requests.exceptions.ConnectionError:
                continue
            except requests.exceptions.ReadTimeout:
                continue
        else:
            test = 'http://' + url
            test2 = 'https://' + url
    # s = requests.session()
    # s.keep_alive = False
            try:
                req = requests.get(test2,timeout=0.1,headers=headers)
                reqcode = req.status_code
                if reqcode == 200:
                    urlalive.append(test2)
                else:
                    urlalive.append(test)
            except requests.exceptions.ConnectTimeout:
                urldead.append(test)
            except requests.exceptions.ConnectionError:
                continue
            except requests.exceptions.ReadTimeout:
                continue
    print(f'存活url个数:{len(urlalive)}')

def get_title(text):
    soup = BeautifulSoup(text,'lxml')
    title = soup.title
    if title != None:
        title = title.string
    return title

def get_thread(number=10):
    pool = Pool(number)
    return pool


class Info:
    '''提取网页的信息'''
    def __init__(self,url):
        self.url = url

    def title(self):
        text = requests.get(self.url,timeout=2,headers=headers).content
        title = get_title(text)
        return title

    #爆破目录
def dirBurp(url):
    with open('dir.txt','r',encoding='utf-8') as f:
        dics = f.readlines()
        for dic in dics:
            dic = dic.replace('\n','').replace('\r','')
            line = f'{url}/{dic}'
            try:
                code = requests.get(line,timeout=1,headers=headers).status_code
                if (code == 200) or (code == 302):
                    dirlist.append(f'{line}   <<<status:{code}>>>')
            except Exception as e:
                continue
        return dirlist

start_time = time.time()
print('----开始任务----')
get_url('urls.txt')
resultlist = []

for url in urlalive:
    test = Info(url)
    result = f'{test.url} {test.title()}'
    resultlist.append(result)
    print(result)

pool = get_thread()
pool.map(dirBurp,urlalive)

filepath = f'{os.getcwd()}/result/result.txt'
with open(filepath,'w',encoding='utf-8') as f:
    f.write('\n'.join(resultlist))
    f.write('\n')
    f.write('\n'.join(dirlist))
end_time = time.time()
cast_time = end_time - start_time
print('----任务结束----')
print(f'耗时: {cast_time}')