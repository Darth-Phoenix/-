from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_mysqldb import MySQL
import MySQLdb
import time

app=Flask(__name__)
app.secret_key="123454321"

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="qwerty1234"
app.config["MYSQL_DB"]="login"
db=MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        if 'email' in request.form and 'password' in request.form:
            email=request.form['email']
            password=request.form['password']
            cursor=db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM logininfo WHERE email=%s AND password=%s", (email, password))
            global info
            info=cursor.fetchone()
            if info is not None:
                session['loginsuccess']=True
                return redirect(url_for('profile'))
            else:
                return render_template("login.html")
    return render_template("login.html")

@app.route('/new', methods=['GET', 'POST'])
def new_user():
    if request.method=='POST':
        if "one" in request.form and "two" in request.form and "three" in request.form and "four" in request.form:
            username=request.form['one']
            email=request.form['two']
            password=request.form['three']
            password2=request.form['four']
            cursor=db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM login.logininfo WHERE name=%s OR email=%s", (username, email))
            new=cursor.fetchone()
            if new is None and password != "" and username != "" and email != "" and password == password2:
                cursor.execute("INSERT INTO login.logininfo(name, email, password) VALUES (%s,%s,%s)", (username, email, password))
                db.connection.commit()
                return redirect(url_for('index'))
            else:
                return redirect(url_for('new_user'))
    return render_template("register.html")

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    global info
    if request.method=='POST' and session['loginsuccess']==True:
        if "comment" in request.form:
            comment=request.form['comment']
            if comment!="":
                cursor=db.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("INSERT INTO login.comments(username, time, comment) VALUES (%s,%s, %s)", (info['name'], time.strftime("%Y/%m/%d %H:%M:%S"), comment))
                db.connection.commit()
                return redirect(url_for('profile'))
            else:
                return redirect(url_for('profile'))
    if session['loginsuccess']==True:
        cursor=db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM login.comments ORDER BY id DESC")
        data=cursor.fetchall()
        return render_template("profile.html", info=info, data=data)
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session['loginsuccess']=False
    return redirect(url_for('index'))
    
if __name__=='__main__':
    app.run(debug=True)

