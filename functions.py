#coding:utf8
import calculate

import time
import re
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from bs4 import BeautifulSoup

import cv2
import pytesseract
from PIL import Image,ImageEnhance,ImageFilter
pytesseract.pytesseract.tesseract_cmd = 'F:\\Tesseract-OCR\\tesseract.exe'   ##換成自己的

def get_check_code(driver):
    #get_pic
    code_img=driver.find_element_by_id('authImage')
    code_img.screenshot('code_img.png')
    #去噪
    im=Image.open('code_img.png')
    im=im.resize((270,99),Image.ANTIALIAS)
    #im.show()
    im_gray=im.convert('L')
    im_two=im_gray.point(lambda x:255 if x>135 else 0) ##色值>129 為全白 否則 黑    
    #im_two.show()
    config=('-1 eng')# --oem 1 --psm 10')
    check_code=pytesseract.image_to_string(im_two,config=config)
    rep={'0':'O','1':'I','2':'Z','4':'A','5':'S','7':'J','8':'S','.':'',
         '|':'I',"/":'I','%':'X','$':'S','*':'','¥':'Y',';':'J','￡':'L','!':'I','}':'J'}
    text=check_code.replace(" ","")
    for i in rep:
        text=text.replace(i,rep[i])
    #print(text.upper())
    return text.upper()

def get_data(driver,a):
    time.sleep(1)
    driver.find_element_by_link_text('教務系統').click()
    time.sleep(1)
    driver.find_element_by_link_text('學業成績查詢專區').click()
    time.sleep(1)
    
    url = 'https://aps-course.ntut.edu.tw/StuQuery/LoginSID.jsp&apOu=aa_003_LB&sso=big5&datetime1=1576904404080'
    client = requests.Session()
    res = client.get(url)
      
    url='https://aps-course.ntut.edu.tw/StuQuery/QryScore.jsp'
    driver.get(url)
    res = client.get(url)
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/form/input[3]').click()   ##歷年
    time.sleep(1)

    source=driver.page_source

    #老柯
    soup2=BeautifulSoup(source,"lxml")
    #print(soup2.text)
    ulist=[]
    trs=soup2.find_all("tr")
    for tr in trs:
        ui=[]
        for th in tr:
            ui.append(th.text.strip().replace(u'\u3000',u''))
##        print(ui)
        ulist.append(ui)
    col_name=ulist[0]
    need_list=[]
    for i in ulist:
        if len(i)==8:
            need_list.append(i)
    while col_name in need_list:
        need_list.remove(col_name)
    #print(need_list)

    b=calculate.cal(need_list,a)
    return b
  
def f_total(a):
    ntut='https://aps.ntut.edu.tw/course/tw/Cprog.jsp?format=-3&year=105&matric=7'
    res=requests.get(ntut)
    soup=BeautifulSoup(res.text,"html.parser")
    time.sleep(1)
    
    tr_tags=soup.find_all('tr')
    data_list=tr_tags[0].getText().replace(' ','').split('\n')
    print(data_list[data_list.index('%s'%a):data_list.index('%s'%a)+9])

def main():
    c=input('系所:')
    f_total(c)
    #i_school()
    
if __name__ == '__main__':
    main()

