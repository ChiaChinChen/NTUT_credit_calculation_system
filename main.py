import functions
import time
import re
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from bs4 import BeautifulSoup

from PyQt5 import QtWidgets, QtGui,QtCore
from ui_credits_calculation import Ui_MainWindow
from PyQt5.QtCore import Qt
import sys

class MainWindow(QtWidgets.QMainWindow):
    global driver
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        ##放入標準
        self.ui.label_6.clear()
        self.ui.label_6.setPixmap(QtGui.QPixmap('picture 2.jpg'))
        self.ui.label_6.setScaledContents(True)  #自動對圖片進行縮放
        self.ui.label_19.setPixmap(QtGui.QPixmap('youtube.png'))
        self.ui.label_6.setScaledContents(True)
        # MainWindow 標題
        self.setWindowTitle('計算學分系統!!')
   
        #combobox(寫進系所/學籍)
        years=['105','106','107','108']
        self.ui.comboBox_year.addItems(years)  #設定學籍
        major=['電機系','化工系','材資系【材料組】','材資系【資源組】','土木系','分子系','電子系','工管系',
               '工設系【產品設計組】','工設系【家具與室內設計組】','建築系','車輛系','能源冷凍空調系','英文系',
               '經管系','資工系','光電系','機電學士班【車輛工程系】','機電學士班【能源與冷凍空調工程系】',
               '機電學士班【機械工程系精密機電組】','機電學士班【機械工程系精密設計組】',
               '機電學士班【機械工程系電機與控制組】','電資學士班【電機工程系】',
               '電資學士班【電子工程系】','電資學士班【資訊工程系】','電資學士班【光電工程系】',
               '工程科技學士班【化學工程與生物科技系】','工程科技學士班【材料及資源工程系材料組】',
               '工程科技學士班【材料及資源工程系資源組】','工程科技學士班【土木工程系】',
               '創意設計學士班【工業設計系產品設計組】','創意設計學士班【工業設計系家具與室內設計組】',
               '創意設計學士班【建築系】','創意設計學士班【互動設計系媒體設計組】',
               '創意設計學士班【互動設計系視覺傳達設計組】','文發系','資財系','互動系【媒體設計組】',
               '互動系【視覺傳達設計組】']        
        self.ui.comboBox_major.addItems(major)  #設定系所
        self.ui.comboBox_year.currentIndexChanged.connect(self.select)
        self.ui.comboBox_major.currentIndexChanged.connect(self.select)
        self.ui.pushButton.clicked.connect(self.using_check)

        
    def i_school(self):
        #抓ischool driver and authcode
        global driver
        ##隱藏網頁
        chrome_options=Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        #chrome_options.add_argument('user-data-dir=selenium')
        exe_path='chromedriver.exe'  ##換成自己的
        url = 'https://nportal.ntut.edu.tw'
        client = requests.Session()
        driver = webdriver.Chrome(executable_path=exe_path,chrome_options=chrome_options)
        driver.get(url)
        time.sleep(1)
        self.get_authcode(driver)
    

    def get_authcode(self,driver):
        ##顯示驗證碼
        code_img=driver.find_element_by_id('authImage')
        code_img.screenshot('code_img.png')
        self.ui.label_17.clear()
        self.ui.label_17.setPixmap(QtGui.QPixmap('code_img.png'))
        self.ui.label_17.setScaledContents(True)  #自動對圖片進行縮放

    def using_check(self):
        global driver
        #是否有帳號使用中
        if 'https://nportal.ntut.edu.tw' not in driver.current_url:
            print('先前帳號已登出\n請再次登入新帳號...')
            self.ui.label_29.setText('先前帳號已登出\n請再次登入新帳號...')
            self.ui.label_29.setAlignment(Qt.AlignLeft)
            self.i_school()
            self.ui.lineEdit_3.clear()
        else:
            self.enter_account()
            
    def enter_account(self):
        global dirver
        #登入
        #自動填入驗證碼
        print('enter account')
        if self.ui.lineEdit_3.text()=='' and functions.get_check_code(driver) !='':
            self.ui.lineEdit_3.setText(functions.get_check_code(driver))
        time.sleep(1)
        self.login()
        
    def login(self):
        global driver
        if self.ui.lineEdit.text()=='' or self.ui.lineEdit_2.text()=='' or self.ui.lineEdit_3.text()=='':
            print('請輸入完整帳號、\n密碼、驗證碼...')
            self.ui.label_29.setText('請輸入完整帳號、\n密碼、驗證碼...')
            self.ui.label_29.setAlignment(Qt.AlignLeft)
            ##msgbox
        else:
            driver.find_element_by_id('muid').send_keys(self.ui.lineEdit.text())
            driver.find_element_by_id('mpassword').send_keys(self.ui.lineEdit_2.text()) 
            driver.find_element_by_id('authcode').send_keys(self.ui.lineEdit_3.text())
            driver.find_element_by_class_name('loginBtn').click()
            time.sleep(3)
            self.login_check(driver)
        
    def login_check(self,dirver):
        if 'https://nportal.ntut.edu.tw/myPortal.do?thetime' in driver.current_url:
            print('帳號登入成功!')
            self.ui.label_29.setText('帳號登入成功!')
            self.ui.label_29.setAlignment(Qt.AlignLeft)
            self.auto()
            self.get_data()
            self.gap()
            
        else:
            print('帳號,密碼,驗證碼\n輸入錯誤請重新輸入...')
            self.ui.label_29.setText('帳號,密碼,驗證碼\n輸入錯誤請重新輸入...')
            self.ui.label_29.setAlignment(Qt.AlignLeft)
            driver.find_element_by_class_name('eipButton').click()
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()
            self.ui.lineEdit_3.clear()
            self.get_authcode(driver)
            time.sleep(1)
        return

    def get_data(self):
        print('學分統計中...')
        self.ui.label_29.setText('學分統計中...')
        self.ui.label_29.setAlignment(Qt.AlignLeft)
        #functions.get_data(driver,self.ui.lineEdit.text()[3:5])
        b=[]
        a=functions.get_data(driver,self.ui.lineEdit.text()[3:5])
        for i in range(len(a)):
            b.append(str(a[i]))
        
        self.ui.label_21.setText(b[0])
        self.ui.label_21.setAlignment(Qt.AlignCenter)
        self.ui.label_22.setText(b[1])
        self.ui.label_22.setAlignment(Qt.AlignCenter)
        self.ui.label_23.setText(b[2])
        self.ui.label_23.setAlignment(Qt.AlignCenter)
        self.ui.label_24.setText(b[3])
        self.ui.label_24.setAlignment(Qt.AlignCenter)
        self.ui.label_25.setText(b[4])
        self.ui.label_25.setAlignment(Qt.AlignCenter)
        self.ui.label_26.setText(b[5])
        self.ui.label_26.setAlignment(Qt.AlignCenter)
        self.ui.label_27.setText(b[6])
        self.ui.label_27.setAlignment(Qt.AlignCenter)
##        self.ui.label_28.setText(b[7])
##        self.ui.label_28.setAlignment(Qt.AlignCenter)

        print('學分統計完成!')
        self.ui.label_29.setText('學分統計完成!')
        self.ui.label_29.setAlignment(Qt.AlignLeft)
        


    def Standard(self,a,b):
        ##課程標準
        ntut='https://aps.ntut.edu.tw/course/tw/Cprog.jsp?format=-3&year=%s&matric=7'%b
        res=requests.get(ntut)
        soup=BeautifulSoup(res.text,"html.parser")
        time.sleep(1)
        tr_tags=soup.find_all('tr')
        data_list=tr_tags[0].getText().replace(' ','').split('\n')
        print(data_list[data_list.index('%s'%a):data_list.index('%s'%a)+9])
        c=data_list[data_list.index('%s'%a):data_list.index('%s'%a)+9]
        ##先清除(避免label中有值)
        self.ui.label_2.clear()
        self.ui.label_7.clear()
        self.ui.label_8.clear()
        self.ui.label_9.clear()
        self.ui.label_10.clear()
        self.ui.label_11.clear()
        self.ui.label_12.clear()
        self.ui.label_13.clear()
        self.ui.label_14.clear()
        ##將值放入
        self.ui.label_2.setText(c[0])
        self.ui.label_2.setAlignment(Qt.AlignCenter)
        self.ui.label_7.setText(c[1])
        self.ui.label_7.setAlignment(Qt.AlignCenter)
        self.ui.label_8.setText(c[2])
        self.ui.label_8.setAlignment(Qt.AlignCenter)
        self.ui.label_9.setText(c[3])
        self.ui.label_9.setAlignment(Qt.AlignCenter)
        self.ui.label_10.setText(c[4])
        self.ui.label_10.setAlignment(Qt.AlignCenter)
        self.ui.label_11.setText(c[5])
        self.ui.label_11.setAlignment(Qt.AlignCenter)
        self.ui.label_12.setText(c[6])
        self.ui.label_12.setAlignment(Qt.AlignCenter)
        self.ui.label_13.setText(c[7])
        self.ui.label_13.setAlignment(Qt.AlignCenter)
        self.ui.label_14.setText(c[8])
        self.ui.label_14.setAlignment(Qt.AlignCenter)
        
        
    def select(self):
        ##先清除(避免label中有值)       
        self.ui.label_2.clear()
        self.ui.label_7.clear()
        self.ui.label_8.clear()
        self.ui.label_9.clear()
        self.ui.label_10.clear()
        self.ui.label_11.clear()
        self.ui.label_12.clear()
        self.ui.label_13.clear()
        self.ui.label_14.clear()
        ##取得值
        self.Standard(self.ui.comboBox_major.currentText(),self.ui.comboBox_year.currentText())


    def auto(self):
        a=self.ui.lineEdit.text()[3:5]  ##切割出系所
        b=self.ui.lineEdit.text()[0:3]  ##切割出年份

        #索引'系所'字典
        management={'30':"機械系",'31':"電機系",'32':"化工系",'33':"材資系【材料組】",'34':"土木系",'35':"分子系",
                    '36':"電子系",'37':"工管系",'38':"工設系【產品設計組】",'39':"建築系",'40':"車輛系",'41':"能源冷凍空調系",
                    '42':"英文系",'43':"經管系",'44':"資工系",'45':"光電系",'46':"機電學士班【機械工程系】",'47':"電資學士班【電機工程系】",'48':"工程科技學士班【化學工程與生物科技系】",
                    '49':"創意設計學士班【工業設計系產品設計組】",'50':"文發系",'54':"資財系",'55':"互動系【媒體設計組】"}        
        self.Standard(management[a],b)
        

    def gap(self):
        print('學分差距統計中...')
        self.ui.label_29.setText('學分差距統計中...')
        self.ui.label_29.setAlignment(Qt.AlignLeft)
        
        self.ui.label_32.setText(str(int(self.ui.label_7.text())-float(self.ui.label_21.text())))
        self.ui.label_32.setAlignment(Qt.AlignCenter)
        self.ui.label_33.setText(str(int(self.ui.label_8.text())-float(self.ui.label_22.text())))
        self.ui.label_33.setAlignment(Qt.AlignCenter)
        self.ui.label_34.setText(str(int(self.ui.label_9.text())-float(self.ui.label_23.text())))
        self.ui.label_34.setAlignment(Qt.AlignCenter)
        self.ui.label_35.setText(str(int(self.ui.label_10.text())-float(self.ui.label_24.text())))
        self.ui.label_35.setAlignment(Qt.AlignCenter)
        self.ui.label_36.setText(str(int(self.ui.label_11.text())-float(self.ui.label_25.text())))
        self.ui.label_36.setAlignment(Qt.AlignCenter)
        self.ui.label_37.setText(str(int(self.ui.label_12.text())-float(self.ui.label_26.text())))
        self.ui.label_37.setAlignment(Qt.AlignCenter)
        self.ui.label_38.setText(str(int(self.ui.label_13.text())-float(self.ui.label_27.text())))
        self.ui.label_38.setAlignment(Qt.AlignCenter)

        print('學分差距統計完成!')
        self.ui.label_29.setText('學分差距統計完成!')
        self.ui.label_29.setAlignment(Qt.AlignLeft)
        
        
        
        

    

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    window.i_school()
    sys.exit(app.exec_())




