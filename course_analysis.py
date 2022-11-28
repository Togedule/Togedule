import datetime
import requests
import pandas
import csv
from bs4 import BeautifulSoup # Select 可能不只一個結果，Find 則是特定結果
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
}

def analysis(account):
    htmlfile = "./webarchive/" + str(account) + "_courseinfo.html" #產生動態檔名
    try:
        with open(htmlfile, "r", encoding="big5") as web:
            soup = BeautifulSoup(web, "lxml")
            #因為所下載的課程表格在 html 採用 row-a row-b 輪流呈現，這邊寫法會比較麻煩
            tablehouse = soup.find("div", {"id": "page"})
            table = tablehouse.select("tr")
            data = []
            for row in table:
                data.append(row.text.strip().split('\n')) #這邊的空格與換行處理相對單純
            for i in range(len(data)):
                for j in range(len(data[i])):
                    data[i][j] = data[i][j].strip()
                print(data[i]) 
            # data 是一條一條的課程資訊，裏頭會依序放流水號、課號、課程識別碼、班次、課程名稱、學分、教師姓名、備註
            df = pandas.DataFrame({
                data[0][0]: [data[i][0] for i in range(1,len(data))],
                data[0][1]: [data[i][1] for i in range(1,len(data))],
                data[0][2]: [data[i][2] for i in range(1,len(data))],
                data[0][3]: [data[i][3] for i in range(1,len(data))],
                data[0][4]: [data[i][4] for i in range(1,len(data))],
                data[0][5]: [data[i][5] for i in range(1,len(data))],
                data[0][6]: [data[i][6] for i in range(1,len(data))],
            })
            print(df)
            #但是我把備註那一欄幹掉了，因為我看大家的課程備註都是空的，加了反而困擾
            tablefile = "./webarchive/" + str(account) + "_courseinfo.csv"
            df.to_csv(tablefile, index=False, encoding='big5')
            # index=False 的意思是不要添加序號的 Column 進去 csv 檔
    except:
        pass
    finally:
        pass #有效的帳號才能進行分析，無效的就不要幹活

collect_coursetime = []
collect_location = []

def classroom(course_id, courseclass, semester, account):
    table_url = 'https://nol.ntu.edu.tw/nol/coursesearch/print_table.php?'
    payload = {
        'course_id': course_id,
        'class': courseclass,
        'semester': semester,
        'lang': 'CH'
    } #事實上 payload 有很多 parameters ，但我只能從 courseinfo 現有的資訊放進去搜尋
    record = requests.session()
    visit = record.get(table_url, headers=headers, params=payload)
    visit.encoding="utf-8"
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
    #台大課程網的顯示方式很討厭，所有元件都沒有賦予 id 或 class，只好硬幹
    
    seperate = []
    for i in range(0,len(info),2):
        try:
            seperate.append([info[i].text.strip(), info[i+1].text.strip().replace(u'\xa0', u' ').replace(u'\xfc', u' ')])
        except:
            pass
        # 幹掉 big5 無法處理的特殊字元 \xa0 \xfc，以及剩下空格，再有其他的就算了，反正後面內容不重要
    temp_tablefile = "./webarchive/" + str(account) + "_singleinfo.csv"
    df = pandas.DataFrame({})
    df.T.to_csv(temp_tablefile, header=False, encoding='big5', mode='w')
    #每次使用都會清空暫存檔，包含 seperate list 也會重置
    
    for i in range(len(seperate)-1):
        row = pandas.DataFrame({
            seperate[i][0]: [seperate[i][1]]
        })
        #print(row)
        row.T.to_csv(temp_tablefile, header=False, encoding='big5', mode='a')
    #將單一課程下載 html 後寫入暫存檔
    
    temp = open(temp_tablefile, 'r', encoding='big5')
    fetch = csv.reader(temp)
    for row in fetch:
        if row[0] == '上課時間':
            collect_coursetime.append(row[1])
        if row[0] == '上課地點':
            collect_location.append(row[1])
    temp.close()
    # collect_coursetime 跟 collect_location 為 Global List，也省得 return
    try:
        with open('./temp_downloadpage.html', "w", encoding="utf-8") as savepage:
            savepage.writelines(visit.text)
    except:
        with open('./temp_downloadpage.html', "x", encoding="utf-8") as savepage:
            savepage.writelines(visit.text)
    finally:
        pass

def collect_moreinfo(account):
    try:
        tablefile = "./webarchive/" + str(account) + "_courseinfo.csv"
        database = open(tablefile, 'r', encoding="big5")
        csvreader = csv.reader(database)
        rows, courseid, courseclass, semester = [], [], [], []
        for row in csvreader:
            rows.append(row)
        for i in range(1,len(rows)):
            courseid.append(rows[i][rows[0].index('課程識別碼')])
            courseclass.append(rows[i][rows[0].index('班次')])
            semester.append(check_semester())
        database.close() #因為等一下 classroom 函數會編輯這個檔案，所以先關掉
        
        for i in range(len(courseid)):
            classroom(courseid[i], courseclass[i], semester[i], account)
        print(courseid)
        print(courseclass)
        print(semester)
        print(collect_coursetime)
        print(collect_location)
        
        #database = open(tablefile, 'a', encoding="big5")
        #csvwriter = csv.writer(database)
        moredf = pandas.DataFrame({
            '學期': [semester[i] for i in range(len(semester))],
            '上課時間': [collect_coursetime[i] for i in range(len(collect_coursetime))],
            '上課地點': [collect_location[i] for i in range(len(collect_location))]
        })
        addition = pandas.read_csv(tablefile, encoding='big5')
        totaldata = addition.join(moredf)
        print(totaldata)
        total_tablefile = "./webarchive/" + str(account) + "_totalcourseinfo.csv"
        totaldata.to_csv(total_tablefile, index=False, encoding='big5')
        #為求方便，直接用 pandas 排版並且合併，直接塞入新檔案
    except:
        pass # https://www.geeksforgeeks.org/get-column-names-from-csv-using-python/
    
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

#collect_moreinfo('b08501012')