# coding=utf-8
import requests
import csv
import random
import time
import socket
#python 2.7写法
#import httplib
#python 3.0写法
import http.client
# import urllib.request
from bs4 import BeautifulSoup
import re

def get_content(url , data = None):
    header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url,headers = header,timeout = timeout)
            rep.encoding = 'utf-8'
            # req = urllib.request.Request(url, data, header)
            # response = urllib.request.urlopen(req, timeout=timeout)
            # html1 = response.read().decode('UTF-8', errors='ignore')
            # response.close()
            break
        # except urllib.request.HTTPError as e:
        #         print( '1:', e)
        #         time.sleep(random.choice(range(5, 10)))
        #
        # except urllib.request.URLError as e:
        #     print( '2:', e)
        #     time.sleep(random.choice(range(5, 10)))
        except socket.timeout as e:
            print( '3:', e)
            time.sleep(random.choice(range(8,15)))

        except socket.error as e:
            print( '4:', e)
            time.sleep(random.choice(range(20, 60)))
        #except httplib.BadStatusLine as e:
        except http.client.BadStatusLine as e:
            print( '5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print( '6:', e)
            time.sleep(random.choice(range(5, 15)))

    return rep.text
    # return html_text

def get_data(html_text):
    final = []
    bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body # 获取body部分
    a = body.find('a', {'class': 'mkapp-btn mab-download'})
    val = []
    onclick = a.get('onclick')
    st=onclick.split(',')
    #正则消除特殊符号
    st[1]=re.sub('[\'\(\)]', '', st[1])
    val.append(st[1]) #名称
    st[5]=re.sub('[\'\(\)]','', st[5])
    val.append(st[5]) #apk
    st[6] = re.sub('[\'\(\)\;]', '', st[6])
    val.append(st[6]) #版本
    li=body.find_all('li',{'class': 'ul-li-detail'})
    date = li[1].find('span').string
    val.append(date)
    final.append(val)
    #for info in li:
    #    value = []
    #button=body.find('div', {'class': 'app-function nofloat'}) #找到apk所在按钮
    #onclick=button.get('onclick')
    #final.append(onclick)
    #final.append(button)
    return final

def write_data(data, name):
    file_name = name
    with open(file_name, 'a', errors='ignore', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(data)


if __name__ == '__main__':
    url ='http://app.hicloud.com/app/C10652857'
    html = get_content(url)
    result = get_data(html)
    write_data(result, 'apk.csv')
