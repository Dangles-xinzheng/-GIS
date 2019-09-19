# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 18:06:50 2019

@author: Dell
"""
from urllib import request
import time
from bs4 import BeautifulSoup

def getKeyWords():
    url = "http://poi.mapbar.com/guilin/F10/"
    page = request.urlopen(url)
    data = page.read().decode('utf-8')
    soup = BeautifulSoup(data,'html.parser')
    print(soup)
    tags = soup.select('dd a')
    res = [t.get_text() for t in tags]
    print (res)
    writeTxt(res,'guilin.txt')
# 存储为文本
def writeTxt(data,path):
    file = open(path,"w")
    for ele in data:
        file.write(ele+'\n')
    file.close()           

if __name__ == '__main__':
    print("开始爬取")
    s_time=time.time()
    
    getKeyWords()  
    
    e_time=time.time()
    print("程序共耗时： %.2f s!" % (e_time - s_time))
    
    
    