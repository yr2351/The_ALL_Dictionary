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
def hello_world():
    return 'signin page'

@app.route('/signin', methods =['GET', 'POST'])
def signin():
    msg = ''
    if request.method == 'POST' and 'userID' in request.form and 'password' in request.form:
        userID = request.form['userID']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM UserAccount WHERE userID = % s AND password = % s', (userID, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['userID'] = account['userID']
            msg = 'Logged in successfully !'
            return render_template('html/search.html', msg = msg)
        else:
            msg = 'Incorrect userID / password !'
    return render_template('html/signin.html', msg = msg)
  
@app.route('/signout')
def signout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('userID', None)
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True) 