from flask import request, render_template, Flask
import MySQLdb
app = Flask(__name__)

def connect():
    con = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="T318k512",
        db="usertable",
        use_unicode=True,
        charset="utf8")
    return con


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
