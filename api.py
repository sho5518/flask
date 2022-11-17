from flask import Flask, request, jsonify, render_template
import dicttoxml
import MySQLdb
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

@app.route("/")
def home():
    return render_template("search.html")