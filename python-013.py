# -*- coding: utf-8 -*-

import tkinter as tk
import requests
import time
import pafy
import cv2
from selenium import webdriver
from bs4 import BeautifulSoup


# ===    爬channel-group  ==============================================================

def findtitle(num):
    HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64 ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    url = 'https://monitor.wfuapp.com/2022/12/fulong-beach.html'
    webpage = requests.get(url, headers=HEADERS)
    
    driver = webdriver.Chrome()
    driver.get(url)
    
    time.sleep(3)  
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    listt = []
    
    
    
    divs = soup.find_all('div',class_='channel-group')[num]
    # print(divs)   
    
    lis = divs.find_all('li')
    # print(lis)
   
    try:
        for i in lis:    
            title = i.find('a')
            httpp = 'https://monitor.wfuapp.com/'+title['href']
            print(httpp)
            newtitle = title.text+'     網址:'+httpp
            listt.append(newtitle)
            
    except:
        print()
    
    tt = tuple(listt)
    print(tt)
    menu.set((tt))
    
    
    # time.sleep(2)
    driver.quit()#關閉瀏覽器 
    
# ===    爬youtubeURL   ==============================================================

def findyoutubeURL(url):
   HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64 ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
   url = url
   webpage = requests.get(url, headers=HEADERS)

   driver = webdriver.Chrome()
   driver.get(url)

   time.sleep(3)  

   soup = BeautifulSoup(driver.page_source, 'html.parser')


   divs = soup.find_all('iframe')[1]
   ans = divs['src']
   ans = ans.split('?')[0]


   newans = ans.replace('embed/', 'watch?v=')

   print(newans)   
   return newans


# ===   opencv   ==============================================================

def opencv(urll):
    
    face_cascade = cv2.CascadeClassifier('C:/Users/Admin/Desktop/haarcascade_fullbody.xml')


    url = urll     #士林官邸

    video = pafy.new(url)
    best = video.getbest(preftype="mp4")

    cap = cv2.VideoCapture(best.url)


    while True:
        _, img = cap.read()

        # 轉成灰階
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 偵測臉部
        faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=3,
        minSize=(25, 25))

        # 繪製人臉部份的方框
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 0), 2)

        # 顯示成果
        
        cv2.imshow('img', img)
        #計算找到幾張臉
        print("找到了 {0} 個行人.".format(len(faces)))

        # 按下ESC結束程式執行
        k = cv2.waitKey(30) & 0xff
        if k==27:
            break
    # Release the VideoCapture object     
    cap.release()
    cv2.destroyAllWindows()
 
    
# =====   listbox 顯示   ======================================================



root = tk.Tk()
root.title('景點影像查詢')
root.geometry('800x600')



# ===== 按鈕功能 ======

def button_event(button,n):
    findtitle(n)
   

mybutton1 = tk.Button(root, text='台北 1')
mybutton1.configure(command=lambda: button_event(mybutton1,0))
mybutton2 = tk.Button(root, text='台北 2')
mybutton2.configure(command=lambda: button_event(mybutton2,1))
mybutton1.place(x=80,y=30)
mybutton2.place(x=140,y=30)
tk.Button(root, text='新北',command=lambda: button_event(mybutton2,2)).place(x=205,y=30)
tk.Button(root, text='桃園',command=lambda: button_event(mybutton2,3)).place(x=260,y=30)
tk.Button(root, text='竹苗',command=lambda: button_event(mybutton2,4)).place(x=320,y=30)
tk.Button(root, text='台中',command=lambda: button_event(mybutton2,5)).place(x=380,y=30)
tk.Button(root, text='彰投',command=lambda: button_event(mybutton2,6)).place(x=440,y=30)
tk.Button(root, text='雲嘉',command=lambda: button_event(mybutton2,7)).place(x=500,y=30)
tk.Button(root, text='台南',command=lambda: button_event(mybutton2,8)).place(x=560,y=30)
tk.Button(root, text='高雄',command=lambda: button_event(mybutton2,9)).place(x=620,y=30)
tk.Button(root, text='屏東',command=lambda: button_event(mybutton2,10)).place(x=680,y=30)
tk.Button(root, text='基隆',command=lambda: button_event(mybutton2,11)).place(x=80,y=80)
tk.Button(root, text='宜蘭',command=lambda: button_event(mybutton2,12)).place(x=140,y=80)
tk.Button(root, text='花東',command=lambda: button_event(mybutton2,13)).place(x=200,y=80)
tk.Button(root, text='外島',command=lambda: button_event(mybutton2,14)).place(x=260,y=80)


# ====    listbox   =========

frame = tk.Frame(root, width=15)        # 加入頁框元件，設定寬度
frame.place(x=80,y=150)

scrollbar = tk.Scrollbar(frame)         # 在頁框中加入捲軸元件
scrollbar.pack(side='right', fill='y')  # 設定捲軸的位置以及填滿方式

menu = tk.StringVar()

# 在頁框中加入 Listbox 元件，設定 yscrollcommand = scrollbar.set
listbox = tk.Listbox(frame,  listvariable=menu, height=20, width=90, yscrollcommand = scrollbar.set)

listbox.selection_set(1)    #新加

listbox.pack(side='left', fill='y')    # 設定 Listbox 的位置以及填滿方式
scrollbar.config(command = listbox.yview)  # 設定 scrollbar 的 command = listbox.yview



# ======  查詢功能  =======
def get_selected_options():
    selected=listbox.curselection()
    # label_1.config(text="curselection=" + str(selected))
    # selected_options=[]
    for i in selected:
        bbb = listbox.get(i)            
        bbb = bbb[bbb.find('網址:')+3:]
    print(bbb,'test')

# 第二次爬youtube網址    
    foropencv = findyoutubeURL(bbb) 
# 把網址給opencv     
    opencv(foropencv)   


tk.Button(root, text="確 定",font=15,bg='deepskyblue', width=20,command=get_selected_options).place(x=310,y=500)

root.mainloop()






