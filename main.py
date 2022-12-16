from flask import request, render_template, Flask, jsonify, session, redirect
from werkzeug.security import generate_password_hash as gph
from werkzeug.security import check_password_hash as cph
from datetime import timedelta
import MySQLdb
import secrets
import html

def connect():
    con = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="T318k512",
        db="usertable",
        use_unicode=True,
        charset="utf8")
    return con

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
app.permanent_session_lifetime = timedelta(minutes=60)

password = "hoge"

@app.route("/home")
def home():
    if "username" in session:
        username=session["username"]
        con =connect()
        cur = con.cursor()
        cur.execute("""
                    SELECT weight
                    FORM userlist
                    WHERE username=%(username)s""",{"username":username})
        data=[]
        for row in cur:
            data.append(row)
        weight=data[0][0]
        con.close()
        return render_template("mypage.html",
        weight=weight,
        username=html.escape(session["username"]))
    else:
        return redirect("login")

@app.route("/make", methods={"GET", "POST"})
def make():
    if request.method == "GET":
        return render_template("make.html")
    elif request.method == "POST":
        username = request.form["usermane"]
        sex = request.form["format"]
        age = request.form["age"]
        weight = request.form["weight"]
        password = request.form["password"]
        hashpass = gph(password)
        
        con = connect()
        cur = con.cursor()
        cur.execute("""
        SELECT * FROM userlist WHERE username=%(username)s""",
        {"username":username})
        data=[]
        for row in cur:
           data.append(row)
        if len(data)!=0:
           return render_template("make.html", msg="このユーザー名は使用されています")
        con.commit()
        con.close()
        
        con = connect()
        cur = con.cursor()
        cur.execute("""
        INSERT INTO userlist
        (username,sex,age,password,weight)
        VALUES (%(username)s,%(sex)s,%(age)s,%(hashpass)s,%(weight)s)""",
        {"username":username, "sex":sex, "age":age, "hashpass":hashpass, "weight":weight})
        con.commit()
        con.close()
        return render_template("info.html", username=username, sex=sex, age=age, password=password, weight=weight)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method =="GET":
        session.clear()
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        con = connect()
        cur = con.cursor()
        cur.execute("""
                    SELECT username, sex, age, password, weight
                    FROM userlist
                    WHERE username=%(username)s AND password=%(password)s
                    """,{"username":username, "password":password})
        data=[]
        for row in cur:
            data.append(row[0],row[1],row[2],row[3],row[4])
        if len(data)==0:
            con.close()
            return render_template("login.html", msg="ユーザー名が間違っています")
        if cph(data[0], password):
            session["username"] = data[0][0]
            session["sex"] = data[0][1]
            con.close()
            return redirect("home")
        else:
            con.close()
            return render_template("login.html", "パスワードが間違っています")

@app.route("/search")
def root_page():
    return render_template("search.html")

@app.route("/search", methods=["GET","POST"])
def root_page():
    if request.method == "GET":
        return render_template("search.html")
    elif request.method == "POST":
        sex = request.form["format1"]
        form = request.form["format2"]
        con = connect()
        cur = con.cursor()
        
        if sex =="M":
            con = connect()
            cur = con.cursor()
            cur.execute("""
                        SELECT username,sex,work,date,calorie
                        FROM recoad
                        WHERE sex='M' AND date > DATE_SUB(now(), INTERVAL 30DAY)
                        """)
        elif sex == "F":
            con = connect()
            cur = con.cursor()
            cur.execute("""
                        SELECT username,sex,work,date,calorie
                        FROM recoad
                        WHERE sex='F' AND date > DATE_SUB(now(), INTERVAL 30DAY)
                        """)

        res = {}
        resp = {}
        tmpa = []
        for row in cur:
            dic = {}
            dic["username"] = row[0]
            dic["sex"] = row[1]
            dic["work"] = row[2]
            dic["date"] = row[3]
            dic["calorie"] = row[4]
            tmpa.append(dic)
        res["content"] = tmpa
        con.commit()
        con.close()

        if form == "JSON":
            return render_template("api.html",res=res)
        elif form == "XML":
            xml = dicttoxmil(dic)
            resp = make_response(xml)
            resp.mimetype = "text/xml"
            return resp

@app.route("/result")
def result():

    form = request.args.get("format")
    username = request.args.get("username")

    con = connect()
    cur = con.cursor()
    cur.execute("""
                SELECT username, sex, age, weight
                FROM userlist
                WHERE username=%(username)s
                """,{"username":username})

    res = "<title>検索結果</title>"
    for row in cur:
        res = res + "<table border=\"1\">\n"
        res = res + "\t<tr><td><a href=\"api?id=" + html.escape(str(row[1])) + "&"
        res = res + "format=" + html.escape(form) + "\">" + html.escape(row[0]) + "</a></td></tr>\n"
        res = res + "\t<tr><td><pre>" + html.escape(row[0]) + "</pre></td></tr>"
        res = res + "</table>"
    con.close()
    return res

@app.route('/recoad',methods=["GET","POST"])
def inout():
    if request.method == "GET":
        return render_template("recoad.html")
    elif request.method == "POST":
        calorie = request.form["calorie"]
        calorie = float(calorie)
        if "username" in session:
            username = session["username"]
            sex =session["sex"]

            con = connect()
            cur = con.cursor()
            cur.execute("""
                        INSERT
                        INTO recoad (username,sex,work,date,calorie)
                        VALUES ('username','sex','work','date','calorie')""")
            con.commit()
            con.close()
        

if __name__ == "__main__":
    app.run(host="0.0.0.0")