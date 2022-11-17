from flask import request, render_template, Flask, jsonify
import MySQLdb
import html

app = Flask(__name__)

from werkzeug.security import generate_password_hash as gph
from werkzeug.security import check_password_hash as cph

def connect():
    con = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="T318k512",
        db="usertable",
        use_unicode=True,
        charset="utf8")
    return con

password = "hoge"

@app.route("/")
def home():
    return render_template("search.html")

@app.route("/make", methods={"GET", "POST"})
def make():
    if request.method == "GET":
        return render_template("make.html")
    elif request.method == "POST":
        username = request.form["usermane"]
        sex = request.form["sex"]
        age = request.form["age"]
        weight = request.form["weight"]
        password = request.form["password"]
        hashpass = gph(password)
        con = connect()
        cur = con.cursor()
        cur.execute("""
                    SELECT * FROM list WHERE username=%(username)s
                    """,{"username":username})
        data=[]
        for row in cur:
           data.apend(row)
        if len(data)!=0:
           return render_template("make.html", msg="このユーザー名は使用されています")
        con.commit()
        con.close()
        con = connect()
        cur = con.cursor()
        cur.execute("""
                    INSERT INTO list
                    (username,sex,age,password,weight)
                    VALUES (%(username)s,%(sex)s,%(age)s,%(hashpass)s,%(weight)s)
                    """,{"username":username, "sex":sex, "age":age, "hashpass":hashpass, "weight":weight})
        con.commit()
        con.close()
        return render_template("info.html", username=username, sex=sex, age=age, password=password, weight=weight)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method =="GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        con = connect()
        cur = con.cursor()
        cur.execute("""
                    SELECT passwor FROM list WHERE username=%(username)s
                    """,{"username":username})
        data=[]
        for row in cur:
            data.append(row[0])
        if len(data)==0:
            con.close()
            return render_template("login.html", msg="ユーザー名が間違っています")
        if cph(data[0], password):
            con.close()
            return "ログインしました"
        else:
            con.close()
            return render_template("login.html", "パスワードが間違っています")

@app.route("/result")
def result():
    form = request.args.get("format")
    name = request.args.get("name")
    con = connect()
    cur = con.cursor()
    cur.execute("""
                SELECT thread_id,title,intro
                FROM thread
                WHERE title like %(title)s OR intro like %(intro)s
                """, {"title" : "%"+name+"%", "intro" :"%"+name+"%"})
    res = "<title>検索結果</title>"
    for row in cur:
        res = res + "<table border=\"1\">\n"
        res = res + "\t<tr><td><a href=\"api?id=" + html.escape(str(row[0])) + "&"
        res = res + "format=" + html.escape(form) + "\">" + html.escape(row[1]) + "</a></td></tr>\n"
        res = res + "\t<tr><td><pre>" + html.escape(row[2]) + "</pre></td></tr>"
        res = res + "</table>"
    con.close()
    return res

if __name__ == "__main__":
    app.run(host="0.0.0.0")