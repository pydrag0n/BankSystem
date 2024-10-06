from flask import Flask, render_template, request, session, redirect, url_for
from datetime import timedelta

from db import *
# from auth import UserManager, User, Card
from random import randint

UserOBJ = UserManager()
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4ads00299kkksaoo-0TTGAGAY89===adasdas320-=k0r2'


@app.route("/")
def mainpage():
    return "Index.html"

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if not (session.get('username') is None):
        return redirect(url_for("user_profile"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confim_passwd = request.form.get("repeat_password")
        print(password, confim_passwd)
        if password == confim_passwd and confim_passwd != None and password != None:
            user = User(username, password)
            err_type, not_err = UserOBJ.register(user, confim_passwd)
            print(not_err)
            print(err_type)
            
            if not_err:
                session['username'] = username

                return redirect(url_for('user_profile'))

    return render_template("signup.html")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if not (session.get('username') is None):
        return redirect(url_for("user_profile"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User(username, password)
        err_type, not_err = UserOBJ.authenticate(user)
        print(err_type, not_err)
        if not_err:
            session['username'] = username
            
            return redirect(url_for("user_profile"))
            
    return render_template("signin.html")

@app.route("/user_profile")
def user_profile():

    if not (session.get('username') is None):
        cash = 0
        return render_template("user_profile.html", cash=cash)
    else:
        return redirect(url_for('signin'))

@app.route("/admin")
def admin():
    return "asd"

@app.route("/logout", methods=["GET", "POST"])
def logout():
    if not (session.get('username') is None):
        session.pop('username', None)
        return redirect(url_for('signin'))
    return redirect(url_for('signin'))

if __name__ == "__main__":
    app.run(debug=True)