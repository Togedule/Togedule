# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 11:16:38 2022

@author: finge
"""

import csv
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
import os #刪除紀錄好的.csv


def initialize():
    try:
        cred = credentials.Certificate("./serviceAccount.json")
        app = firebase_admin.initialize_app(cred)
        #execute once when first time using this program 
    except:
        pass

def create_database(account, password = None):
    initialize()
    store = firestore.client()
    file_path = "./webarchive/{}_totalcourseinfo.csv".format(account)
    ParentCollection = "StudentID"
    ParentDoc = account
    doc_ref = store.collection(ParentCollection).document(ParentDoc)
    doc_ref.set({ParentCollection:ParentDoc}) 
    collection_name = "course"
    # StudentID(collection) => 學號(doc) => course(collection) => 各課程資訊(doc)
    # 指定文件路徑(doc_ref)，使用set去建立文件，其中input必須是dictionary

    def batch_data(iterable, n=1):
        l = len(iterable)
        for ndx in range(0, l, n):
            yield iterable[ndx:min(ndx + n, l)]
        # 讓list(data)中的每個item分開儲存成一個item
        # eg. [{1, 2}, {3, 4}] => [1, 2, 3, 4]
    
    data = []
    headers = []
    with open(file_path, encoding='Big5') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                for header in row:
                    headers.append(header)
                line_count += 1
            else:
                obj = {}
                for idx, item in enumerate(row):
                    obj[headers[idx]] = item
                data.append(obj) #data是list，用一個dict儲存一堂課的所有info
                line_count += 1
        print(f'Processed {line_count} lines.')
    
    for batched_data in batch_data(data, 499):
        batch = store.batch()
        for data_item in batched_data:
            doc_ref = store.collection(ParentCollection).document(ParentDoc).collection(collection_name).document(data_item.get('課程名稱'))
            batch.set(doc_ref, data_item)
        batch.commit()
    print('Done')
    os.remove(file_path)  #刪除匯入完成的.csv檔
    
# 測試
#create_database('b08603001')
# 班次待改

def get_singleCourseInfo(account, course, password = None):
    # 給定課程名稱，回傳單一課程資訊
    initialize()
    store = firestore.client()
    ParentCollection = "StudentID"
    ParentDoc = account
    collection_name = "course"
    # path = "{}/{}/{}/{}".format(ParentCollection, ParentDoc, collection_name, course)
    # StudentID(collection) => 學號(doc) => course(collection) => 各課程資訊(doc)
    doc_ref = store.collection(ParentCollection).document(ParentDoc).collection(collection_name).document(course) 
    doc = doc_ref.get()
    if doc.exists:
        # print(f'Document data: {doc.to_dict()}') # 透過 to_dict()將文件轉為dictionary
        return doc.to_dict()
    else:
        print(u'No such document!')

# 測試: 輸入學號和課程名稱
#singleCourse= get_singleCourseInfo('b08603001', '日文二上')
#print(singleCourse)

def get_allCourseInfo(account, password = None):
    Clst=[]  #course list
    # 給定帳號，回傳所有課程資訊
    initialize()
    store = firestore.client()
    ParentCollection = "StudentID"
    ParentDoc = account
    collection_name = "course"
    
    student = store.collection(ParentCollection).document(ParentDoc).get()
    collection_ref = store.collection(ParentCollection).document(ParentDoc).collection(collection_name)
    docs = collection_ref.get()
    if student.exists:
         for doc in docs:
             Clst.append(doc.to_dict())
             # print("文件內容：{}".format(doc.to_dict()))
         return Clst
    else:
        print(u'This account does not exist!')

# 測試: 輸入學號
allCourse = get_allCourseInfo('b08603001')


def get_fields(Clst):
    #取得所有的課程中的欄位(名稱、地點、時間)
    Nlst = []
    Plst = []
    Tlst = []
    for i in range(len(Clst)):
        name = Clst[i].get('課程名稱')
        place = Clst[i].get('上課地點')
        time = Clst[i].get('上課時間')
        Nlst.append(name)
        Plst.append(place)
        Tlst.append(time)
    return Nlst, Plst, Tlst


# 測試: 輸入get_allCourseInfo的list結果
#a, b, c = get_fields(allCourse)
#print(a)

'''
TO-DO
def make_table(allCourse)
def timeplace_sorter(allCourse)
def update(account)
'''