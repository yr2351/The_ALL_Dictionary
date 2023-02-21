from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__, template_folder='../web_views')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '0000'
app.config['MYSQL_DB'] = 'cse416'

mysql = MySQL(app)

@app.route('/')
def search():
    return render_template("html/search.html")

@app.route('/signup', methods =['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST' and 'userID' in request.form and 'password' in request.form and 'email' in request.form and 'name' in request.form and 'nickname' in request.form and 'phoneNumber' in request.form:
        userID = request.form['userID']
        isAdmin = False
        fullName = request.form['name']
        nickName = request.form['nickname']
        password = request.form['password']
        email = request.form['email']
        phoneNumber = request.form['phoneNumber']
        isPremium = False

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account WHERE userID = % s', (userID, ))
        account = cursor.fetchone()
        #print(account)
        if account:
            msg = 'Account already exists !'
        elif not userID or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO account VALUES (%s, %s)', (userID, isAdmin))
            cursor.execute('INSERT INTO useraccount VALUES (%s, %s, %s, %s, %s, %s, %s, NULL)', (fullName, nickName, userID, password, email, phoneNumber, isPremium, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'

    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    print(msg)
    return render_template('./html/signup.html')

if __name__ == '__main__':
    app.run(debug=True)        # Debug mode will reload files when changed.
