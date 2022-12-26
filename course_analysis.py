import datetime
import requests
import pandas
import csv
import os
from bs4 import BeautifulSoup # Select 可能不只一個結果，Find 則是特定結果

# 萬能模擬瀏覽器，這個檔案完全不需要登入帳號密碼
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
}
# 常用陣列變數，依序蒐集某一個同學的所有上課時間與地點
# collect_coursetime 跟 collect_location 為 Global List，不急著 return
collect_coursetime = []
collect_location = []

# 協助將 {account}_courseinfo.html 轉換成 {account}_courseinfo.csv
def transfer_courseinfo(account):
    # {account}_courseinfo.html 要從 request.py 的 download_student_info 取得
    temp_tablehtml = "./webarchive/" + str(account) + "_courseinfo.html"
    try:
        with open(temp_tablehtml, "r", encoding="big5") as web:
            soup = BeautifulSoup(web, "lxml")
            # 所下載的課程 html 在表格採用 row-a row-b 輪流呈現，這邊寫法需要客製化一下
            tablehouse = soup.find("div", {"id": "page"})
            table = tablehouse.select("tr")
            data = []
            for row in table:
                data.append(row.text.strip().split('\n')) #這邊的空格與換行處理相對單純
            for i in range(len(data)):
                for j in range(len(data[i])):
                    data[i][j] = data[i][j].strip()
            # data 是一條一條的資訊，依序存放流水號、課號、課程識別碼、班次、課程名稱、學分、教師姓名、備註
            # 但是我把備註那一欄幹掉了，因為我看大家的課程備註都是空的，加了反而困擾
            # 可能有備註是寫說密集課程之類的，但我們就不管了
            df = pandas.DataFrame({
                data[0][0]: [data[i][0] for i in range(1,len(data))],
                data[0][1]: [data[i][1] for i in range(1,len(data))],
                data[0][2]: [data[i][2] for i in range(1,len(data))],
                data[0][3]: [data[i][3] for i in range(1,len(data))],
                data[0][4]: [data[i][4] for i in range(1,len(data))],
                data[0][5]: [data[i][5] for i in range(1,len(data))],
                data[0][6]: [data[i][6] for i in range(1,len(data))],
            })
            temp_tablecsv = "./webarchive/" + str(account) + "_courseinfo.csv"
            df.to_csv(temp_tablecsv, index=False, encoding='big5')
            # print(df) 可以測試製造的 dataframe 是否有誤
            # index=False 的意思是不要添加序號的 Column 進去 csv 檔
    finally:
        pass
    # 有效的帳號才能進行分析，無效的就不要幹活

# 處理某一個同學的某堂課，到台大課程網抓取上課時間與地點，製造 Global List
def append_singleinfo(course_id, courseclass, semester, account):
    table_url = "https://nol.ntu.edu.tw/nol/coursesearch/print_table.php?"
    payload = {
        'course_id': course_id,
        'class': courseclass,
        'semester': semester,
        'lang': 'CH'
    }
    # 事實上 payload 有很多 parameters ，但我只能從 courseinfo 現有的資訊放進去搜尋
    record = requests.session()
    visit = record.get(table_url, headers=headers, params=payload)
    visit.encoding="utf-8"
    # print(len(visit.text)) 測試這個網站可以下載多少條有效字串
    soup = BeautifulSoup(visit.text, "lxml")
    bigtable = soup.findAll("table", {
        "cellspacing":0, 
        "bordercolordark":"#ffffff",
        "cellpadding": 2,
        "width": "100%",
        "bordercolorlight": "#666666",
        "border": 1
        })[1]
    smalltable = bigtable.find("tbody")
    info = smalltable.select("td")
    # 台大課程網的顯示方式很討厭，所有元件都沒有賦予 id 或 class，只好硬幹特徵
    
    seperate = []
    for i in range(0,28,2):
        try:
            seperate.append([info[i].text.strip(), info[i+1].text.strip().replace(u'\xa0', u' ').replace(u'\xfc', u' ')])
        except:
            seperate.append(['',''])
        finally:
            pass
        # 原本是 len(info)，但考慮到簡體字打不上去，所以不要製造完整的暫存檔
        # 幹掉 big5 無法處理的特殊字元 \xa0 \xfc，以及剩下空格，再有其他的就算了，反正後面內容不重要
        # except 在這裡失效，因為發指令給系統做事情出包了，python 並不會知道
    temp_singlecsv = "./webarchive/" + str(account) + "_singleinfo.csv"
    df = pandas.DataFrame({})
    df.T.to_csv(temp_singlecsv, header=False, encoding='big5', mode='w')
    # 每次使用都要清空暫存檔，包含 seperate list 也會重置，這裡我們先寫「空白」進去
    
    for i in range(len(seperate)-1):
        row = pandas.DataFrame({
            seperate[i][0]: [seperate[i][1]]
        })
        #print(row)
        row.T.to_csv(temp_singlecsv, header=False, encoding='big5', mode='a')
    # 現在才可以將單一課程的 html 寫進 csv 暫存（已經分成兩欄）
    
    temp = open(temp_singlecsv, 'r', encoding='big5')
    fetch = csv.reader(temp)
    for row in fetch:
        if row[0] == '上課時間':
            collect_coursetime.append(row[1])
        if row[0] == '上課地點':
            collect_location.append(row[1])
    temp.close()
    # 然後再讀取這個暫存 csv ，尋找我們要的上課時間與地點
    # collect_coursetime 跟 collect_location 為 Global List，不急著 return
    
    temp_singlehtml = "./webarchive/" + str(account) + "_singleinfo.html"
    try:
        with open(temp_singlehtml, "w", encoding="utf-8") as savepage:
            savepage.writelines(visit.text)
    except:
        with open(temp_singlehtml, "x", encoding="utf-8") as savepage:
            savepage.writelines(visit.text)
    finally:
        pass
    # 每一次使用此函數，都會覆蓋一遍 {account}_singleinfo.csv
    # 順便留存最近一次覆蓋的 {account}_singleinfo.html 作檢查用

# 將 {account}_courseinfo.csv 擴增為 {account}_totalcourseinfo.csv
# 接手 transfer_courseinfo，擴增課程資訊，重複呼叫 append_singleinfo
def combine_moreinfo(account):
    try:
        temp_tablecsv = "./webarchive/" + str(account) + "_courseinfo.csv"
        database = open(temp_tablecsv, 'r', encoding="big5")
        csvreader = csv.reader(database)
        rows, courseid, courseclass, semester = [], [], [], []
        for row in csvreader:
            rows.append(row)
        for i in range(1,len(rows)):
            courseid.append(rows[i][rows[0].index('課程識別碼')])
            courseclass.append(rows[i][rows[0].index('班次')])
            semester.append(check_semester())
        database.close()
        # 因為等一下 append_singleinfo 函數會編輯這個檔案，所以先關掉
        # 這裡可以檢查 print(courseid) 或 print(courseclass) 或 print(semester)
        for i in range(len(courseid)):
            append_singleinfo(str(courseid[i]), str(courseclass[i]), str(semester[i]), str(account))
        
        '''
        database = open(tablefile, 'a', encoding="big5")
        csvwriter = csv.writer(database)
        這個方法會出包，因為不能寫成 column
        '''
        moredf = pandas.DataFrame({
            '學期': [semester[i] for i in range(len(semester))],
            '上課時間': [collect_coursetime[i] for i in range(len(collect_coursetime))],
            '上課地點': [collect_location[i] for i in range(len(collect_location))]
        })
        addition = pandas.read_csv(temp_tablecsv, encoding='big5')
        totaldata = addition.join(moredf)
        total_tablefile = "./webarchive/" + str(account) + "_totalcourseinfo.csv"
        totaldata.to_csv(total_tablefile, index=False, encoding='big5')
        print(totaldata) # 最後檢查用
        # 為求方便，直接叫 pandas 讀取排版並且合併，直接塞入新檔案
        # 參考網站： https://www.geeksforgeeks.org/get-column-names-from-csv-using-python/
    finally:
        # print(collect_coursetime)
        # print(collect_location)
        collect_coursetime.clear()
        collect_location.clear()
    # Global List 功成身退請重置
    
# 回傳該學期為何，例如 "111-1"
def check_semester():
    today = datetime.datetime.now()
    year = today.year
    month = today.month
    day = today.day
    if month >= 9 or month <= 2:
        year_ROC = year - 1911
        section = 1
    if month >= 3 and month <= 8:
        year_ROC = year - 1911 + 1
        section = 2
    return str(year_ROC) + "-" + str(section)

# 刪除暫存檔案，只留下 {account}_totalcourseinfo.csv 給資料庫處理
def clear_temp_docs(account):
    # 必須輸入乾淨的學生帳號，小寫而且去掉信箱
    temp_tablehtml = "./webarchive/" + str(account) + "_courseinfo.html"
    temp_tablecsv = "./webarchive/" + str(account) + "_courseinfo.csv"
    temp_singlehtml = "./webarchive/" + str(account) + "_singleinfo.html"
    temp_singlecsv = "./webarchive/" + str(account) + "_singleinfo.csv"
    # 上述文件恰為當初的下載順序
    temporaries = [temp_tablehtml, temp_tablecsv, temp_singlehtml, temp_singlecsv]
    for i in range(len(temporaries)):
        if os.path.isfile(temporaries[i]):
            os.remove(temporaries[i])

# 測試專區
# transfer_courseinfo("b08501012")
# combine_moreinfo("b08501012")
# clear_temp_docs("b08501012")