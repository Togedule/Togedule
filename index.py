from flask import (Flask, request, render_template, redirect , url_for , session, flash)
from request_ntu import logincheck
from datetime import timedelta

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return self.username, self.password

app = Flask(__name__)
app.config['SECRET_KEY'] = 'BF5lRODqNxfQ*o*#kU(r#9uMX#xHseWNISl7W1!D' # 設定flask的密鑰secret_key。要先替flask設定好secret_key，Flask-Login 才能運作。
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=60)

@app.route('/',methods=['GET'])
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

                return redirect(url_for('profile', realname = realname))

        except logincheck(username,password) == False:
                alert = '帳密輸入錯誤 請重新嘗試'
                return redirect(url_for('login'), alert = alert)
        
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/registration',methods=['GET','POST'])
def registration():
    if request.method == 'GET':  # 輸入網址會進到這裡
        render_template('login.html')

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

                return redirect(url_for('profile'))

        except TypeError:
                return redirect(url_for('registration'))

        return redirect(url_for('registration'))
    return render_template('registration.html')

@app.route('/<realname>',methods=['GET','POST'])
def profile(realname):
    realname = session.get('realname')
    alert = '請登入帳號：Please login.'

    if request.method == 'GET':  # 輸入網址會進到這裡
        if realname :
            return render_template('profile.html', realname = realname)    
        return render_template('login.html',alert = alert)

@app.route('/logout')
def logout():
    session.clear()
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5500,debug=True)

#python index.py