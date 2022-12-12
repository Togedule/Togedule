from flask import (Flask, request, render_template, redirect , url_for)
from request_ntu import logincheck

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return self.username, self.password

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',title="Home")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = str(request.form['username'])
        password = str(request.form['password'])

        try:
            if logincheck(username,password) != False:   #新的判斷法
            #user = [x for x in users if x.username == username][0]   #準備幹掉
            #if user and user.password == password:
                #username = user.username.upper()
                realname = logincheck(username,password)
                username = username.upper()
                #name = realname.name
                return redirect(url_for('profile', realname = realname))

        except IndexError:
                return redirect(url_for('login'))

        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/<realname>')
def profile(realname):

    return render_template('profile.html', realname = realname)

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5500,debug=True)