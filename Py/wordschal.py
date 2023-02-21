from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__, template_folder = '../template')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '0000'
app.config['MYSQL_DB'] = 'cse416'

mysql = MySQL(app)

@app.route("/wcquiz", methods = ['GET'])
def quiz():
    if request.method == 'GET':
        quest=request.form

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM WordsChallenge')
        WordsChallenge = cursor.fetchall()
        return render_template("wcquiz.html", quest = WordsChallenge)

@app.route("/wcresult", methods = ['POST'])
def result():
    count = 0
    for i in quest.keys():
        answered = request.form[i]

if __name__ == "__main__":
    app.run(debug = True)