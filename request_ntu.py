import requests
#import pandas as pd
#from bs4 import BeautifulSoup
from course_analysis import analysis, classroom, collect_moreinfo

login_url = 'https://web2.cc.ntu.edu.tw/p/s/login2/p1.php'
secure_url = 'https://if177.aca.ntu.edu.tw/qcaureg/index.asp'

username = input("輸入帳號：")
password = input("輸入密碼：")

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
login = record.get('https://if177.aca.ntu.edu.tw/qcaureg/stulogin.asp', headers=headers)
login = record.post('https://web2.cc.ntu.edu.tw/p/s/login2/p1.php', headers=headers, data=payload)
login = record.get('https://if177.aca.ntu.edu.tw/qcaureg/index.asp', headers=headers)
login.encoding = "big5"
print(login.text)

htmlfile = "./webarchive/" + str(username) + "_courseinfo.html"
try:
    with open(htmlfile, 'x', encoding='big5') as write:
        write.writelines(login.text)
except:
    with open(htmlfile, 'w', encoding='big5') as write:
        write.writelines(login.text)
else:
    pass
finally:
    pass

analysis(username)
collect_moreinfo(username)

'''
11/18 筆記
使用者登入在 https://web2.cc.ntu.edu.tw/p/s/login2/p1.php
可是全新的 p1.php 因為沒有指定登入以後要去哪裡，預設會退回 https://my.ntu.edu.tw/
所以要先透過主腦 myntu 告訴模擬瀏覽器要使用什麼功能
進入 https://web2.cc.ntu.edu.tw/p/s/login2/p1.php ，採 POST 模式才能輸入
台大課程網、選課結果系統都是用
payload = {
    'user': 'b0XXXXXXX'
    'pass': '12345678abc'
    'submit': '登入'
}

params=payload 這是東吳那邊的打法， payload=payload 網站看不懂

選課結果查詢會碰到的第一個連結 https://if177.aca.ntu.edu.tw/qcaureg/stulogin.asp
緊接著自動導向至 https://web2.cc.ntu.edu.tw/p/s/login2/p1.php 這個時候 p1.php 才有意義

參考網站 https://github.com/ChenKB91/better_courses
'''