import re

import requests
import xlrd
from bs4 import BeautifulSoup
from xlutils.copy import copy



# 获取html
def getHtmlText(url, code="GBK"):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'}
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return "获取html异常"


# 解析地区，返回地区清单
'''
def getGroundList(htext):
    try:
        grounddict = {}
        soup = BeautifulSoup(htext, "html.parser")
        gdname = soup.find('dl', attrs={'class':'nobackground'})
        keyList = gdname.find_all('a')
        for i in range(1,len(keyList)):
            key = keyList[i].text
            val = keyList[i].get('href')
            grounddict[key] = val
        return grounddict
    except:
        print("getGroundList异常")
'''


# 解析页码
def getPageCode(htext, typeitem):
    try:
        soup = BeautifulSoup(htext, "html.parser")
        s1 = soup.find('a', attrs={'class': 'last'})
        if (s1):
            pat = re.compile(typeitem + r'pn([0-9]+).html')
            if (s1.get('href')):
                code = pat.search(s1.get('href'))
                if (code):
                    return code.group(1)
        else:
            return 0

    except:
        print("getPageCode异常")


# 解析学校信息，返回学校名称、地址、电话、网址
def getSchoolList(htext, fileAddress, cityitem, typeitem):
    try:
        schoolDict = {}
        soup = BeautifulSoup(htext, "html.parser")
        sclist1 = soup.find_all('dl', attrs={'class': 'left'})
        sclist2 = soup.find_all('dl', attrs={'class': 'right'})
        sclist = sclist1 + sclist2
        for item in sclist:
            schoolDict['城市'] = cityitem
            schoolDict['类型'] = typeitem
            schoolDict['学习名称'] = item.find('p').text
            sl = item.find_all('li')
            schoolDict['地址'] = sl[0].text
            schoolDict['电话'] = sl[1].text
            schoolDict['网址'] = sl[2].text
            #schoolDict['地址'] =schoolDict['地址'].replace("地址：","")
            #schoolDict['电话'] = schoolDict['电话'].replace("电话：", "")
            #schoolDict['网址'] = schoolDict['网址'].replace("网址：", "")
            # f = open(fileAddress, 'a', encoding='utf-8')
            # f.write(str(schoolDict)  + '\n' )

            savefile(schoolDict, fileAddress)
    except:
        print("getSchoolList异常")


# 保存到excel
def savefile(schoolDict, fileAddress):
    workbook = xlrd.open_workbook(fileAddress, 'w+b')
    sheet = workbook.sheet_by_index(0)
    wb = copy(workbook)
    ws = wb.get_sheet(0)
    rowNum = sheet.nrows
    ws.write(rowNum, 0, schoolDict['城市'])
    ws.write(rowNum, 1, schoolDict['类型'])
    ws.write(rowNum, 2, schoolDict['学习名称'])
    ws.write(rowNum, 3, schoolDict['地址'])
    ws.write(rowNum, 4, schoolDict['电话'])
    ws.write(rowNum, 5, schoolDict['网址'])

    wb.save(fileAddress)


# 获取城市列表,城市由EXCEL文件存储
def getCityList():
    try:
        cityFileAddress = r'D:\name.xlsx'
        file = xlrd.open_workbook(cityFileAddress)
        sheet = file.sheet_by_name('A')
        cityDic = {}
        for i in range(sheet.nrows):
            key = sheet.col_values(0)[i]
            value = sheet.col_values(1)[i].lower()
            cityDic[key] = value
        return cityDic
    except:
        print("getCityList失败")


def main():
    cityList = getCityList()
    typeList = {'小学': '/xiaoxue/', '初中': '/chuzhong/'}
    for cityitem in cityList:
        for typeitem in typeList:
            searchUrl = 'http://' + cityList[cityitem] + '.xuexiaodaquan.com'
            fileAddress = 'D:/小学与初中.xls'
            htext = getHtmlText(searchUrl + typeList[typeitem])
            getSchoolList(htext, fileAddress, cityitem, typeitem)
            pagecode = int(getPageCode(htext, typeList[typeitem]))
            if pagecode != 0:
                for i in range(2, pagecode + 1):
                    h1text = getHtmlText(searchUrl + typeList[typeitem] + 'pn' + str(i) + '.html')
                    getSchoolList(h1text, fileAddress, cityitem, typeitem)


main()
