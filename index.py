from flask import (Flask, request, render_template, redirect , url_for , session)
from request_ntu import logincheck
from datetime import timedelta
from combine_request_firestore import school_timetable,re_htmlcode
from map_pic import map_pic_white

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return self.username, self.password

app = Flask(__name__)
app.config['SECRET_KEY'] = 'BF5lRODqNxfQ*o*#kU(r#9uMX#xHseWNISl7W1!D' # 設定flask的密鑰secret_key。要先替flask設定好secret_key，Flask-Login 才能運作。
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=60)

@app.route('/',methods=['GET'])  # 輸入網址會進到這裡
def index():
    if 'realname' in session:  # 偵測使用者是否登錄過
        realname = session['realname']
    else: 
        realname = None
    return render_template('index.html', realname = realname)


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':  # 輸入網址會進到這裡
        render_template('login.html')

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        try:
            if logincheck(username,password) != False:
                realname = logincheck(username,password)
                session['username'] = username
                session['password'] = password
                session['realname'] = realname
                session.permanent = True #設定section有Timeout
                map_pic_white(username)

                return redirect(url_for('profile', realname = realname))

        except logincheck(username,password) == False: 
            None

        else:
            alert = '帳密輸入錯誤 請重新嘗試'
            return render_template('login.html', alert = alert)
        
    return render_template('login.html')


@app.route('/registration',methods=['GET','POST'])
def registration():

    alert = "····· 首次註冊需花費10~20秒蒐集遠端資料 ·····請耐心等候"
    if request.method == 'GET':  # 輸入網址會進到這裡
        render_template('registration.html', alert = alert)

    realname = ""
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        try:
            if logincheck(username,password) != False:
                realname = logincheck(username,password)
                session['username'] = username
                session['password'] = password
                session['realname'] = realname
                session.permanent = True #設定section有Timeout
                map_pic_white(username)

                #table = school_timetable(username, password)
                #session['table'] = table
                return redirect(url_for('profile', realname = realname))

        except logincheck(username,password) == False: 
            None

        else:
            alert = '················· 學校系統查無此帳密 ················· 請重新輸入'
            return render_template('registration.html', alert = alert)
    
    return render_template('registration.html', alert = alert)

"""
@app.route('/waiting')
def waiting():
    username = session.get('username')
    realname = session.get('realname')
    
    return redirect(url_for('profile', realname = realname))
"""

@app.route('/<realname>',methods=['GET','POST'])
def profile(realname):
    username = session.get('username')
    password = session.get('password')
    table = school_timetable(username, password)

    if request.method == 'GET':  # 輸入網址會進到這裡
        alert = '請登入帳號：Please login.'

        if realname :
            return render_template('profile.html', realname = realname, table = table)    
        return render_template('login.html',alert = alert)

@app.route('/logout')
def logout():
    session.clear()
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5500,debug=True)