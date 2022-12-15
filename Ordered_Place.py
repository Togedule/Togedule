'''
#測資:簡易版
Clst = ['Python程式設計基礎課程', '專題研究一', '專題討論一', '日文二上', 
'簡報製作與表達', '食品加工學', '食品加工實驗', '食品工程學', '食品微生物學']
Plst = ['管一B01', '', '農化二B10', '共307', '普102', '農化一第六-1', '食科102', '食科102', '食科102']
Tlst = ['星期一2,3,4(9:10~12:10)', '', '星期二8,9(15:30~17:20)', '星期五2,3,4(9:10~12:10)', 
'星期三A,B,C(18:25~21:05)', '星期四1,2,6(8:10~14:10)', '星期一6,7(13:20~15:10)', 
'星期五6,7,8(13:20~16:20)', '星期三2,3,4(9:10~12:10)']

#測資: 困難版
Clst = ['學士論文上', '專題討論一', '德文一上', '植物生物技術概論', '植物養分之攝取與運輸', '社會學', 
'試驗設計學', '重量訓練']
Plst = ['', '農化二B10', '共203共203', '農化二106', '農化二106農化二B10', '共201', '共104共104', '綜館舞蹈室']
Tlst = ['', '星期二8,9(15:30~17:20)', '星期三5,6(12:20~14:10)星期五5,6(12:20~14:10)', 
'星期四8,9(15:30~17:20)', '第1,2,3,4,5,6,7,8,9,10週星期二6,7(13:20~15:10)星期三1,2(8:10~10:00)', 
'星期五7,8,9(14:20~17:20)', '星期四6(13:20~14:10)星期五3,4(10:20~12:10)', '星期一3,4(10:20~12:10)']
'''

from firestore import get_allCourseInfo, get_fields

account = input('輸入學號: ')  #需要是已經註冊aka登陸資料庫的學號
allCourse = get_allCourseInfo(account)
Clst, Plst, Tlst = get_fields(allCourse)
#print(Clst, Plst, Tlst)

#生成乾淨的時間地點
def cleanTPinfo(Clst, Plst, Tlst):
    #移除沒有地點的課程
    while '' in Plst:
        index = Plst.index('')
        Plst.remove('')
        Tlst.remove(Tlst[index])
        Clst.remove(Clst[index])

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
    #print(Clst, Plst, Tlst)
    return Cnum, Cweekday

#按星期幾去分類
def dailyTP_generator(Clst, Plst, Tlst):
    Cnum, Cweekday = cleanTPinfo(Clst, Plst, Tlst)
    Mon, Tue, Wed, Thu, Fri, Sat, Sun = {}, {}, {}, {}, {}, {}, {}
    MonC, TueC, WedC, ThuC, FriC, SatC, SunC = [], [], [], [], [], [], []

    for x in range(len(Clst)):
        for y in range(len(Cweekday[x])):
            if '一' in Cweekday[x][y]:
                Mon[str(Cnum[x][y]).strip('[').strip(']')] = str(Plst[x][y])
                MonC.append(Clst[x])
            elif '二' in Cweekday[x][y]:
                Tue[str(Cnum[x][y]).strip('[').strip(']')] = str(Plst[x][y])
                TueC.append(Clst[x])
            elif '三' in Cweekday[x][y]:
                Wed[str(Cnum[x][y]).strip('[').strip(']')] = str(Plst[x][y])
                WedC.append(Clst[x])
            elif '四' in Cweekday[x][y]:
                Thu[str(Cnum[x][y]).strip('[').strip(']')] = str(Plst[x][y])
                ThuC.append(Clst[x])
            elif '五' in Cweekday[x][y]:
                Fri[str(Cnum[x][y]).strip('[').strip(']')] = str(Plst[x][y])
                FriC.append(Clst[x])
            elif '六' in Cweekday[x][y]:
                Sat[str(Cnum[x][y]).strip('[').strip(']')] = str(Plst[x][y])
                SatC.append(Clst[x])
            elif '日' in Cweekday[x][y]:
                Sun[str(Cnum[x][y]).strip('[').strip(']')] = str(Plst[x][y])
                SunC.append(Clst[x])

    #print('M:', Mon, 'T:', Tue,'W:', Wed,'T:', Thu,'F:', Fri,'S:', Sat,'S:', Sun)
    #print('M:', MonC, 'T:', TueC,'W:', WedC,'T:', ThuC,'F:', FriC,'S:', SatC,'S:', SunC)
    daily_TPdict = [Mon, Tue, Wed, Thu, Fri, Sat, Sun]
    daily_Clst = [MonC, TueC, WedC, ThuC, FriC, SatC, SunC]
    #print(daily_TPdict)
    #print(daily_Clst)

    return daily_TPdict, daily_Clst

daily_TPdict, daily_Clst = dailyTP_generator(Clst, Plst, Tlst)

'''
示範執行結果(簡易版):
daily_TPdict = [{'234': '管一B01', '67': '食科102'}, {'89': '農化二B10'}, {'ABC': '普102', '234': '食科102'}, 
{'126': '農化一第六-1'}, {'234': '共307', '678': '食科102'}, {}, {}]
'''


#排序一天的課程
def order(Clst, Plst, Tlst):
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
        elif len(daily_TPdict[z]) == 0:
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

Plst_order_week = order(Clst, Plst, Tlst)
print(Plst_order_week)


'''
示範執行結果(簡易版):
[['管一B01', '管一B01', '管一B01', '食科102', '食科102'], ['農化二B10', '農化二B10'], 
['普102', '普102', '普102', '食科102', '食科102', '食科102'], ['農化一第六-1', '農化一第六-1', '農化一第六-1'], 
['共307', '共307', '共307', '食科102', '食科102', '食科102'], [None], [None]]
'''

