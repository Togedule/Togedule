from firestore import get_allCourseInfo, get_fields
from tabulate import tabulate

#生成乾淨的時間地點
def cleanTPinfo(allCourse):
    Nlst, Plst, Tlst = get_fields(allCourse)
    #移除沒有地點的課程
    while '' in Plst:
        index = Plst.index('')
        Plst.remove('')
        Tlst.remove(Tlst[index])
        Nlst.remove(Nlst[index])

    #分開不同的上課時間，移除第...週
    for j in range(len(Tlst)):
        while '週' in Tlst[j]:
            index = Tlst[j].index('週')
            Tlst[j] = Tlst[j][index+1:]
        Tlst[j] = str(Tlst[j]).split(')')
        while '' in Tlst[j]:
            Tlst[j].remove('')
        if len(Tlst[j])>1:
            half = int(len(str(Plst[j]))/len(Tlst[j]))  #這句可能會出bug，但教室真的無規律QQ
            Plst[j] = [Plst[j][0:half], Plst[j][half:]]
        else:
            Plst[j] = [Plst[j]]
    #print(Plst)
    #print(Tlst)

    #抓出星期幾&節次
    Cweekday = []
    Cnum = []
    for k in range(len(Tlst)): #k的意義是不同課程
        num_1 =[]
        weekday = []
        for m in range(len(Tlst[k])): #m的意義是同堂課分不同時段上課
            num_2 = []
            weekday.append(Tlst[k][m][2])
            num_2.append(Tlst[k][m][3])
            while ',' in Tlst[k][m]:
                index = Tlst[k][m].index(',')
                num_2.append(Tlst[k][m][index+1])
                Tlst[k][m] = Tlst[k][m][0:index] + Tlst[k][m][index+1:]
            num_2 = ''.join(str(x) for x in num_2)
            num_1.append(num_2)
        Cnum.append(num_1)
        Cweekday.append(weekday)
    #print(Cweekday, Cnum)
    return Nlst, Plst, Tlst, Cnum, Cweekday

#按星期幾去分類
def dailyTP_generator(allCourse):
    Nlst, Plst, Tlst, Cnum, Cweekday = cleanTPinfo(allCourse)
    Mon, Tue, Wed, Thu, Fri, Sat, Sun = {}, {}, {}, {}, {}, {}, {}
    MonC, TueC, WedC, ThuC, FriC, SatC, SunC = [], [], [], [], [], [], []

    for x in range(len(Nlst)):
        for y in range(len(Cweekday[x])):
            if '一' in Cweekday[x][y]:
                Mon[str(Cnum[x][y]).strip('[').strip(']')] = str(Plst[x][y])
                MonC.append(Nlst[x])
            elif '二' in Cweekday[x][y]:
                Tue[str(Cnum[x][y]).strip('[').strip(']')] = str(Plst[x][y])
                TueC.append(Nlst[x])
            elif '三' in Cweekday[x][y]:
                Wed[str(Cnum[x][y]).strip('[').strip(']')] = str(Plst[x][y])
                WedC.append(Nlst[x])
            elif '四' in Cweekday[x][y]:
                Thu[str(Cnum[x][y]).strip('[').strip(']')] = str(Plst[x][y])
                ThuC.append(Nlst[x])
            elif '五' in Cweekday[x][y]:
                Fri[str(Cnum[x][y]).strip('[').strip(']')] = str(Plst[x][y])
                FriC.append(Nlst[x])
            elif '六' in Cweekday[x][y]:
                Sat[str(Cnum[x][y]).strip('[').strip(']')] = str(Plst[x][y])
                SatC.append(Nlst[x])
            elif '日' in Cweekday[x][y]:
                Sun[str(Cnum[x][y]).strip('[').strip(']')] = str(Plst[x][y])
                SunC.append(Nlst[x])

    #print('M:', Mon, 'T:', Tue,'W:', Wed,'T:', Thu,'F:', Fri,'S:', Sat,'S:', Sun)
    #print('M:', MonC, 'T:', TueC,'W:', WedC,'T:', ThuC,'F:', FriC,'S:', SatC,'S:', SunC)
    daily_TPdict = [Mon, Tue, Wed, Thu, Fri, Sat, Sun]
    daily_Nlst = [MonC, TueC, WedC, ThuC, FriC, SatC, SunC]
    #print(daily_TPdict)
    #print(daily_Nlst)

    return daily_TPdict, daily_Nlst
    
#排序一天的課程
def order(allCourse):
    daily_TPdict, daily_Nlst = dailyTP_generator(allCourse)
    Plst_order_week = []
    lst = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'A', 'B', 'C', 'D')
    for z in range(7):  #7天
        Plst_order_day = []
        if len(daily_TPdict[z]) >1:   #每天的課超過一堂才需要排序
            key = list(daily_TPdict[z].keys())
            for index in range(len(key)):
                for hour in lst:
                    if str(hour) in key[index]:
                        #print(daily_TPdict[z].get(key[index]))
                        Plst_order_day.append(daily_TPdict[z].get(key[index]))
        elif len(daily_TPdict[z]) == 0:  #沒有課的日子(eg.正常人的六日)就是None
            Plst_order_day.append(None)
            Plst_order_week.append(Plst_order_day)
            continue
        else:
            key = list(daily_TPdict[z].keys())
            for hour in lst:
                if str(hour) in key[0]:
                    #print(daily_TPdict[z].get(key[0]))
                    Plst_order_day.append(daily_TPdict[z].get(key[0]))
        Plst_order_week.append(Plst_order_day)

    return Plst_order_week

'''
排序地點:
account = input('輸入學號: ')  #需要是已經註冊aka登陸資料庫的學號
allCourse = get_allCourseInfo(account)
Plst_order_week = order(allCourse)
print(Plst_order_week)
'''

#製作表格，預設為html格式
#Supported table formats: https://pypi.org/project/tabulate/
def tableMaker(allCourse, tablefmt='html'):
    daily_TPdict, daily_Nlst = dailyTP_generator(allCourse)
    header = ['','一','二','三','四','五','六','日'] 
    data = []
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
                    hour_data.append('{}\n{}'.format(Cname, Place))
            if len(hour_data) == 1+day:
                hour_data.append('')
        data.append(hour_data)
    #print(tabulate(data, headers=header, tablefmt='grid', stralign="center"))

    return tabulate(data, headers=header, tablefmt=tablefmt, stralign='center')

'''
製作表格:
account = input('輸入學號: ')  #需要是已經註冊aka登陸資料庫的學號
allCourse = get_allCourseInfo(account)
print(tableMaker(allCourse, 'grid'))
'''
#1215 ver.