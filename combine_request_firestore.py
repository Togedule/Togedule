from request_ntu import download_student_info
from firestore import create_database, get_allCourseInfo, update
from Order_and_Table import tableMaker, order, dailyTP_generator
import HTML

def tableMaker_1(allCourse):
    daily_TPdict, daily_Nlst = dailyTP_generator(allCourse)
    header = ['','一','二','三','四','五','六','日'] 
    data = []
    data.append(header)
    lst = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'A', 'B', 'C', 'D')
    for hour in lst:
        hour_data = [hour]
        for day in range(7):
            todayC = daily_Nlst[day]
            todayTP = daily_TPdict[day]
            TP_key = list(daily_TPdict[day].keys())
            for index in range(len(TP_key)):
                if str(hour) in TP_key[index]:
                    Cname = todayC[index]
                    Place = todayTP[TP_key[index]]
                    hour_data.append('{}<br>{}'.format(Cname, Place))
            if len(hour_data) == 1+day:
                hour_data.append('')
        data.append(hour_data)
    return data


#將爬蟲完的資料儲存到firestore
#account = input("輸入帳號：")
#password = input("輸入密碼：")

def school_timetable(account, password):
    #download_student_info(account, password)
    #create_database(account)

    #由firebase取得資料，進行課程時間地點排序並製作課表
    allCourse = get_allCourseInfo(account)
    #Plst_order_week = order(allCourse)   #這個Plst_order_week是給地圖用的
    table = tableMaker(allCourse,'html')   #tableMaker的格式預設為html
    #return(Plst_order_week)  
    return(table)

#更新資訊暫時使用整體刪除再寫入的方式
#update(account, password)

def re_htmlcode(account):
    allCourse = get_allCourseInfo(account)
    table_data = tableMaker_1(allCourse)
    return table_data

#print(re_htmlcode("b07612041"))
