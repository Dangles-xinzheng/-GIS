# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 09:18:59 2019

@author: Dell
"""
from urllib.parse import quote
from urllib import request
import json  
from location import isInBound, get_boundaries 
import xlwt


#定义小矩形边界

poilist = []
#获取小矩形
def get_task_list(corner, delta_y, delta_x):
    '''
    将大矩形区域划分为长delta_x,宽为delta_y的小矩形
    :param corner:
    :param delta_y:
    :param delta_x:
    :return:
    '''
    #存储小矩形
    task_list = []
    j = 0
    while True:
        loc1_y = float(corner['lower_left_corner']['lat']) + j * delta_y
        #当前小矩形左下角纬度超过上边纬度，退出
        if loc1_y >= float(corner['upper_right_corner']['lat']):
            break
        #当前小矩形右上角纬度超过上边纬度，则其值为上边纬度
        if float(corner['lower_left_corner']['lat']) + (j + 1) * delta_y > float(corner['upper_right_corner']['lat']):
            loc2_y = float(corner['upper_right_corner']['lat'])
        else:
            loc2_y = float(corner['lower_left_corner']['lat']) + (j + 1) * delta_y
        i = 0
        while True:
            #当前小矩形左下角经度
            loc1_x = float(corner['lower_left_corner']['lng']) + i * delta_x
            #当前小矩形左下角经度超过右边经度，退出
            if loc1_x >= float(corner['upper_right_corner']['lng']):
                break
            #当前小矩形右边纬度超过右边经度的值，其值为右边经度的值
            if float(corner['lower_left_corner']['lng']) + (i + 1) * delta_x > float(
                    corner['upper_right_corner']['lng']):
                loc2_x = float(corner['upper_right_corner']['lng'])
            else:
                loc2_x = float(corner['lower_left_corner']['lng']) + (i + 1) * delta_x
            #小矩形的左下角和右上角经纬度
            bounds = (loc1_y, loc1_x, loc2_y, loc2_x)
            task_list.append(bounds)
            i += 1
        j += 1
    return task_list

def get_data(bounds, keyword, boundary):
    url0 = 'http://api.map.baidu.com/place/v2/search?'
    ak = 'xxxxxxxxxx'   #自己申请的百度地图开发者的秘钥
    # 矩形区域检索
    for k in range(40):
        url = url0 + 'query=' + quote(keyword) + '&page_size=20&page_num=' + quote(str(k)) + '&scope=1&bounds=' + quote(str(bounds[0])) + ',' + quote(str(bounds[1])) + ','+quote(str(bounds[2])) + ',' + quote(str(bounds[3])) + '&output=json&ak=' + ak     
        data = request.urlopen(url)
        hjson = json.loads(data.read())
        print (hjson)
        if hjson['message'] == 'ok':
            results = hjson['results']          
            for result in results: 
                name = result.get('name')
                location = result.get('location')
                if location:
                    lat = location.get('lat')
                    lng = location.get('lng')
                    point = {'lat': lat, 'lng': lng}
                else:
                    continue
                address = result.get('address')
                # 保存区域内检索结果
                if isInBound(point, boundary):
                    if (address == None):
                        continue
                    poilist.append((name, address,lng, lat))
            #查询存在数据，则保存

def write_to_excel(city, poilist):
    # 一个Workbook对象，这就相当于创建了一个Excel文件
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet("小区",cell_overwrite_ok=True)

    # 第一行(列标题)
    sheet.write(0, 0, 'name')   #兴趣点的地点名称
    sheet.write(0, 1, 'addr')  #兴趣点的地址   
    sheet.write(0, 2, 'lng') #经度
    sheet.write(0, 3, 'lat')#纬度

    count = 1
    for poi in poilist:
        name = poi[0]   #从列表中获取店名
        location = poi[1]   #从列表中获取经纬度   
        lng = poi[2]  #取出经度
        lat = poi[3]

        # 每一行写入
        sheet.write(count, 0, name)
        sheet.write(count, 1, location) 
        sheet.write(count, 2, lng)
        sheet.write(count, 3, lat)
        
        count += 1
    
    # 最后，将以上操作保存到指定的Excel文件中
    book.save(city +'poi.xls')
        
if __name__ == '__main__':
    poilist=[]
    citylist = ['南京市']
    query = '美食' #搜索关键词设置
    for city in citylist:
        boundaries = get_boundaries(city)    #返回城市边界  以及   矩形拐角
        corner = boundaries['corner']        #获取矩形  左下角和右上角
        boundary = boundaries['boundary']    #获取边界
        
        #设置的值越大，划分的小网格越少
        delta_y=0.05    #小网格的纬度差
        delta_x=0.05    #小网格的经度差
        task_list = get_task_list(corner, delta_y, delta_x)   #大矩形划分为小网格
        
        for rectangle in task_list:
            get_data(rectangle,query,boundary)
        
        write_to_excel(city,poilist)
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    