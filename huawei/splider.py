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
import sqlite3

from urllib3.connection import log

db = r"D:\competition.db"
sql= r""
#conn = sqlite3.connect(db)
#cursor=conn.cursor()



def get_content(url , data = None):
    header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
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

    # 添加数据到数据库


def get_data(html_text):
    final = []
    bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body # 获取body部分
    data = body.find('div', {'id': 'recommendAppList'})  # 找到id为recommendAppList的div
    ul = data.find_all('ul')  # 获取所有ul部分
    #li = ul.find_all('li')  # 获取所有的li
    for app in ul:
        val = []
        ico = app.find('li', {'class':'app-ico'}) #找到当前li class为app-ico的内容
        a = ico.find('a')
        url =a.attrs['href']
        val.append('http://app.hicloud.com'+url)
        img=ico.find('img')
        #src=img.attrs['src']
        pic=img.get("lazyload")
        #print(pic)
        val.append(pic)
        title = app.find('li', {'class':'app-title'}).string #app名称
        val.append(title)
        type = app.find('li',{'class':'app-class'}).string
        val.append(type)

        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute("""insert into tab_app (url,pic,name,type) \
                VALUES (?,?,?,?)""", (str(val[0]), str(val[1]), str(val[2]), str(val[3])))
        conn.commit()
        conn.close()

        final.append(val)

    return final

def write_data(data, name):
    file_name = name
    with open(file_name, 'a', errors='ignore', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(data)


if __name__ == '__main__':
    url ='http://app.hicloud.com/'
    html = get_content(url)
    result = get_data(html)
    write_data(result, 'app.csv')
