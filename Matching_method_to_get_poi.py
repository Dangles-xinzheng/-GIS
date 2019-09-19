# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 22:51:26 2019

@author: Dell
"""
from urllib.parse import quote
from urllib import request
import json
import time
import xlwt

#
def getCityCode(cityList):
    cityCodeFile = r'cityCode.txt'
    cityCode = []  #存储城市编号
    cityDic = {}   #存储城市名及其编号的字典
    with open(cityCodeFile, 'r') as file:       
        #遍历，存储文件中的城市及其编号，形成键值对  
        for cityLine in file.readlines():
            line=cityLine.strip('\n')
            c = line.split(",")
           
            cNum = int(c[0])  #城市编号
            cName = c[1]      #城市名称
            c = {cName:cNum}  #形成键值对
            cityDic.update(c) 
        
        #匹配城市编号
        for city in cityList:
            code = cityDic[city]
            cityCode.append(code)
            print (city,code)
            
    return  cityCode
            
    
def getPOI(cityCode):
    poiList = []
    effe = 0
    
    #获取城市编码，如果一次查询很多城市，请自己改写为循环模式
    code = cityCode[0]
    with open(r'guilin.txt','r') as f:
        #循环遍历地址
        for line in f:
            data = []
            wd = line
            
            url = 'http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=s&da_src=searchBox.button&wd='+quote(wd)+'&c='+quote(str(code))+'&pn=0'
            page = request.urlopen(url)
            res = json.load(page)  #获取查询结果
            if 'content' in res:
                contents = res['content']
                if 'acc_flag' in contents[0]:
                    #遍历结果的每一种数据
                    for d in contents:
                        x, y = float(d['diPointX']), float(d['diPointY'])
                        #经纬度
                        ss = "http://api.map.baidu.com/geoconv/v1/?coords=%s,%s&from=6&to=5&ak=bAUE84z2c0SA8Yt8etMEWosP1xHUGIy0"%(x/100.0,y/100.0)
                        pos = json.load(request.urlopen(ss))   #经纬度返回坐标
                        if pos['status']==0:
                            x, y = pos['result'][0]['x'], pos['result'][0]['y']
                        data.append(d['addr']+','+d['area_name']+','+d['name']+','+str(x)+','+str(y))
                        print(d['addr']+','+d['area_name']+','+d['name']+','+str(x)+','+str(y))
            #存在结果，保存
            if data:
                effe += 1
                print("effe:")
                print(effe)
                poiList.append(data)
                
        #写入文件
        write_to_excel(poiList)

# 存储为文本
def write_to_excel(poilist):
    # 一个Workbook对象，这就相当于创建了一个Excel文件
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet("小区",cell_overwrite_ok=True)

    # 第一行(列标题)
    sheet.write(0, 0, 'addr')  #兴趣点的地址
    sheet.write(0, 1, 'area_name')   #兴趣点的地点名称
    sheet.write(0, 2, 'name')   #兴趣点的地点名称
    sheet.write(0, 3, 'lng') #经度
    sheet.write(0, 4, 'lat')#纬度

    count = 1
    for i in range(len(poilist)):
        for poi in poilist[i]:
            data = poi.split(',')

            location = data[0]   #从列表中获取经纬度
            area_name = data[1]   #从列表中获取店名
            name = data[2]   #从列表中获取店名
            lng = data[3]  #取出经度
            lat = data[4]
    
            # 每一行写入
            sheet.write(count, 0, location)
            sheet.write(count, 1, area_name)
            sheet.write(count, 2, name)
            sheet.write(count, 3, lng)
            sheet.write(count, 4, lat)
            
            count += 1



    # 最后，将以上操作保存到指定的Excel文件中
    book.save(r'poi.xls')



if __name__ == '__main__':
    print("开始爬取")
    s_time=time.time()
    
    #输入需要查询的城市
    city= ['桂林市']
    #获取城市编号
    cityCode = getCityCode(city)
    
    getPOI(cityCode) 
    e_time=time.time()
    print("程序共耗时： %.2f s!" % (e_time - s_time))
    
    
    
    
    
    
    
    
    