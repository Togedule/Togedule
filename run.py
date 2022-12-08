from flask import (Flask, request, render_template, redirect , url_for)
import webbrowser

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return self.username, self.password

users = []
users.append(User(username="b07612041",password="123"))
users.append(User(username="b07612042",password="123"))

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
            user = [x for x in users if x.username == username][0]
            if user and user.password == password:
                username = user.username.upper()
                return redirect(url_for('profile', username = username))
                #return redirect(url_for('profile'))

        except IndexError:
                return redirect(url_for('login'))

        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/<username>')
def profile(username):
    username = username.upper()

    return render_template('profile.html', username = username)

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5500,debug=True)