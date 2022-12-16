import requests
from bs4 import BeautifulSoup
# from flask import (Flask, request, render_template, redirect , url_for)
from course_analysis import transfer_courseinfo, combine_moreinfo, clear_temp_docs

#username = input("輸入帳號：")
#password = input("輸入密碼：")
# username = str(request.form['username'])
# password = str(request.form['password'])

# 透過 myntu 檢查學生帳號與密碼是否存在
def check_exist(username, password):
    # 開始嘗試登入
    payload = {
        'user': username,
        'pass': password,
        'Submit': '登入'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    record = requests.session()
    testlogin = record.get('https://my.ntu.edu.tw/', headers=headers)
    testlogin = record.get('https://my.ntu.edu.tw/login.aspx', headers=headers)
    testlogin = record.post('https://web2.cc.ntu.edu.tw/p/s/login2/p1.php', headers=headers, data=payload)
    # testlogin = record.get('https://my.ntu.edu.tw/Default.aspx', headers=headers)
    # 登入成功後，理想上會自動跳轉回 myntu 首頁，所以不必再進行 request。倘若登入失敗，則跳轉到失敗畫面。
    testlogin.encoding = "utf-8"
    testsoup = BeautifulSoup(testlogin.text, "lxml")
    print("Testing login......")
    findid = testsoup.find("div", {"id": "idtext"})
    # 理想上會獲得" 鍾淯全 同學 您好！"，經過整理只要留下前面的姓名
    getname = findid.text.split()[0]
    return(getname)
    # 倘若登入失敗，也不要在這裡用 try except，就讓回傳功能出包，讓後面 logincheck 函數的 try 出包
    
# 專門處理個人課程資訊，全套服務，製造 {account}_totalcourseinfo.csv
def download_student_info(username, password):
    payload = {
        'user': username,
        'pass': password,
        'Submit': '登入'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    # 使用者登入頁面 https://web2.cc.ntu.edu.tw/p/s/login2/p1.php
    # 但是全新的 p1.php 因為沒有指定登入以後要去哪裡，所以會退回 https://my.ntu.edu.tw/
    # 所以要先進去源頭（myntu）告訴模擬瀏覽器要使用什麼功能
    # 選課結果查詢會碰到的第一個連結 https://if177.aca.ntu.edu.tw/qcaureg/stulogin.asp
    # 緊接著自動導向至 https://web2.cc.ntu.edu.tw/p/s/login2/p1.php ，這個時候 p1.php 才有意義
    # 採 POST 模式才能輸入，經測試，台大的寫法是 data=payload 台大的版本
    # （params=payload 東吳的版本，payload=payload 台大看不懂）
    # 參考網站： https://github.com/ChenKB91/better_courses
    record = requests.session()
    login = record.get('https://if177.aca.ntu.edu.tw/qcaureg/stulogin.asp', headers=headers)
    login = record.post('https://web2.cc.ntu.edu.tw/p/s/login2/p1.php', headers=headers, data=payload)
    login = record.get('https://if177.aca.ntu.edu.tw/qcaureg/index.asp', headers=headers)
    login.encoding = "big5"
    # print(login.text)
    htmlfile = "./webarchive/" + str(username) + "_courseinfo.html"
    try:
        with open(htmlfile, 'x', encoding='big5') as write:
            write.writelines(login.text)
    except:
        with open(htmlfile, 'w', encoding='big5') as write:
            write.writelines(login.text)
    finally:
        pass
    
    transfer_courseinfo(username)
    combine_moreinfo(username)
    clear_temp_docs(username)
    # course_analysis.py 會幫忙凱瑞後續檔案撰寫
   
# 這是讓 login.html 的 <form> 提交以後，檢查的第一站，過關了才跳轉個人 profile
def logincheck(username, password):
    try:
        if "@ntu.edu.tw" in str(username):
            username = username.split("@")[0]
        # 先將同學輸入的東西簡化成乾淨的學號，如果本來就很乾淨，那太好了
        username = username.lower()
        # print(username)
        realname = check_exist(username, password)
    except:
        print("登入失敗")
        return False
    else:
        print("登入成功")
        download_student_info(username, password)
        return realname
    finally:
        pass
    # 登入失敗回傳 False，登入成功回傳使用者姓名（當作 True 使用）





# print(logincheck(username, password))
# download_student_info(username, password) 我認為前端應該要另外寫一個按鈕
# Update 20221214