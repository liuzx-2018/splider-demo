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
            break
        except socket.timeout as e:
            print( '3:', e)
            time.sleep(random.choice(range(8,15)))

        except socket.error as e:
            print( '4:', e)
            time.sleep(random.choice(range(20, 60)))
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
    data = body.find('div', {'class': 'city-all'})  # 找到id为recommendAppList的div
    dl = data.find_all('dl')  # 获取所有dl部分
    dd = data.find_all('dd')  # 获取所有dd部分
    #li = ul.find_all('li')  # 获取所有的li
    for app in dd:
        val = []
        title = app.find('a').string #app名称
        val.append(title)

        a = app.find('a')
        url =a.attrs['href']
        val.append(url)

#        conn = sqlite3.connect(db)
#        cursor = conn.cursor()
#        cursor.execute("""insert into tab_app (url,pic,name,type) \
#                VALUES (?,?,?,?)""", (str(val[0]), str(val[1]), str(val[2]), str(val[3])))
#        conn.commit()
#        conn.close()

        final.append(val)

    return final

def write_data(data, name):
    file_name = name
    with open(file_name, 'a', errors='ignore', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(data)


if __name__ == '__main__':
    url ='http://http://www.xuexiaodaquan.com/'
    html = get_content(url)
    result = get_data(html)
    write_data(result, 'D:/daquan.xls')
