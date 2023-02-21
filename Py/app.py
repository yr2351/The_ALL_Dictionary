from flask import flash, Flask, render_template, request, redirect, url_for, session, jsonify
from dictionaries import mwlDict, mwcDict, oxfordDict, googleImageDict, googleNewsDict, urbanDict, wikiDict, youtubeDict
from flask_mysqldb import MySQL
import MySQLdb.cursors
import asyncio
import json
import hashlib
import random
import time, datetime


app = Flask(__name__, template_folder='../static')
app._static_folder = '../static'
app.secret_key = '0000'

app.config['MYSQL_HOST'] = 'database-1.c7y9frxady0i.ap-northeast-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = '87654321'
#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = '0000'
app.config['MYSQL_DB'] = 'cse416'

mysql = MySQL(app)


@app.route('/')
def search():
    if session.get('loginAccount'):
        loginAccount = session['loginAccount']
    else:
        loginAccount = None
    return render_template("html/search.html", loginAccount=loginAccount)


@app.route('/searchResult/<string:word>')
def searchResult(word):
    if session.get('loginAccount'):
        loginAccount = session['loginAccount']
    else:
        loginAccount = None

    # mwl = mwlDict(word)
    # mwc = mwcDict(word)
    # oxford = oxfordDict(word)
    # #etymonline = etymonlineDict(word)
    # googleImage = googleImageDict(word)
    # googleNews = googleNewsDict(word)
    # #synonym = synonymDict(word)
    # #thefreedictionary = thefreedictionaryDict(word)
    # urban = urbanDict(word)
    # wiki = wikiDict(word)
    # #wiktionary = wiktionaryDict(word)
    # #wordnet = wordnetDict(word)
    # youtube = youtubeDict(word)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = mwlDict(word), mwcDict(word), oxfordDict(word), googleImageDict(word), googleNewsDict(word), urbanDict(word), wikiDict(word), youtubeDict(word)
    mwl, mwc, oxford, googleImage, googleNews, urban, wiki, youtube = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

    return render_template("./html/searchResult.html", loginAccount=loginAccount, word=word, mwl=mwl, mwc=mwc, oxford=oxford, googleImage=googleImage, googleNews=googleNews, urban=urban, wiki=wiki, youtube=youtube)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    return render_template('./html/signin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('./html/signup.html')

@app.route('/addUser', methods=['GET', 'POST'])
def addUser():
    email = request.form['email']
    password = request.form['pw']
    md5Password = hashlib.md5(password.encode()).hexdigest()
    name = request.form['name']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f"""SELECT * FROM Account WHERE email = '{email}';""")

    account = cursor.fetchone()

    if account:
        msg = 'Already exist account'
    else:
        isAdmin = 0
        delete = "n"
        cursor.execute(
            f"""INSERT INTO Account VALUES ('{email}', '{isAdmin}', '{delete}');""")
        cursor.execute(
            f"""INSERT INTO UserAccount VALUES ('{email}', '{md5Password}', '{name}', NULL);""")
        mysql.connection.commit()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f"""SELECT * FROM Account WHERE email = '{email}';""")
        loginAccount = cursor.fetchone()

        session['loginAccount'] = loginAccount

        msg = 'Successfully registered'
    return msg

@app.route('/getUserByEmailAndPW', methods=['GET', 'POST'])
def getUserByEmailAndPW():
    email = request.form['email']
    password = request.form['pw']
    md5Password = hashlib.md5(password.encode()).hexdigest()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f"""
        SELECT * FROM UserAccount AS ua
        JOIN Account AS a
        ON ua.email = a.email
        WHERE ua.email= '{email}'AND ua.password='{md5Password}' AND a.del='n'
        """)
    account = cursor.fetchone()

    if account:
        session['loginAccount'] = account
        return 'ok'
    else:
        return 'fail'

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    session.pop('loginAccount', None)
    msg = 'ok'
    return msg

@app.route('/dictOrder')
def dictOrder():
    if session.get('loginAccount') == None:
        return redirect(url_for('signin'))
    return render_template('./html/changeDictionaryOrder.html')

@app.route('/addDicOrder', methods=['POST'])
def addDicOrder():
    number = request.form['number']
    source = request.form['source']
    email = session['loginAccount']['email']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        f"""INSERT INTO HasSourceOrder VALUES ('{email}', '{number}', '{source}') ON DUPLICATE KEY UPDATE source = VALUES(source);""")

    mysql.connection.commit()

    return 'ok'

@app.route('/getAllDic', methods=['GET'])
def getAllDic():
    if session.get('loginAccount'):
        email = session['loginAccount']['email']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            f"""SELECT * FROM HasSourceOrder WHERE email = '{email}';""")

        dic_list = cursor.fetchall()

        return json.dumps(dic_list)
    else:
        return 'fail'

@app.route('/mypage')
def mypage():
    if session.get('loginAccount') == None:
        return redirect(url_for('signin'))

    email = session['loginAccount']['email']
    isAdmin = session['loginAccount']['isAdmin']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f"""SELECT * FROM UserAccount WHERE email = '{email}';""")
    account = cursor.fetchone()

    return render_template('./html/mypage.html', account=account, isAdmin=isAdmin)

@app.route('/addScHis', methods=['POST'])
def addScHis():
    if session.get('loginAccount'):
        email = session['loginAccount']['email']
        word = request.form['word']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            f"""INSERT INTO HasSearchHistory (email,word,regDate) VALUES ('{email}','{word}',SYSDATE());""")

        mysql.connection.commit()

        return 'ok'
    else:
        return 'fail'

@app.route('/addImgUrlToUser', methods=['POST'])
def addImgUrlToUser():
    email = session['loginAccount']['email']
    img_url = request.form['img_url']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        f"""UPDATE UserAccount SET profilePictureURL ='{img_url}' WHERE email= '{email}';""")
    mysql.connection.commit()

    return 'ok'

@app.route('/delUser', methods=['POST'])
def delUser():
    email = session['loginAccount']['email']
    session.pop('loginAccount', None)

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f"""UPDATE Account SET del='y' WHERE email= '{email}';""")
    mysql.connection.commit()

    return 'ok'

@app.route('/changePw', methods=['POST'])
def changePw():
    email = session['loginAccount']['email']
    password = request.form['pw']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        f"""UPDATE UserAccount SET password ='{password}' WHERE email= '{email}';""")
    mysql.connection.commit()

    return 'ok'

@app.route('/changeName', methods=['POST'])
def changeName():
    email = session['loginAccount']['email']
    name = request.form['name']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        f"""UPDATE UserAccount SET name ='{name}' WHERE email= '{email}';""")
    mysql.connection.commit()

    return 'ok'

@app.route('/about')
def about():
    if session.get('loginAccount'):
        loginAccount = session['loginAccount']
    else:
        loginAccount = None
    return render_template("./html/about.html", loginAccount=loginAccount)


#quiz and challenge
@app.route("/wc")
def home():
    if session.get('loginAccount'):
        loginAccount = session['loginAccount']
        isAdmin = session['loginAccount']['isAdmin']
        return render_template("./html/wc.html", loginAccount=loginAccount, isAdmin = isAdmin)
    else:
        loginAccount = None
        isAdmin = None
        return redirect('/signin')

@app.route("/wcquiz", methods=['GET'])
def wcquiz():
    if session.get('loginAccount'):
        loginAccount = session['loginAccount']
        if request.method == 'GET':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM WordsChallenge ORDER BY qid ASC')
            WordsChallenge = cursor.fetchall()
            return render_template("./html/wcquiz.html", quest=WordsChallenge, loginAccount=loginAccount)
    else:
        loginAccount = None
        return redirect('/signin')
    
@app.route("/wcresult", methods=['GET', 'POST'])
def result():
    if session.get('loginAccount'):
        loginAccount = session['loginAccount']
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        i = 0
        count = 0
        qnum = []
        q = []
        rightans = []
        wrongans = []
        email = session['loginAccount']['email']
        answer = request.form.to_dict()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM WordsChallenge ORDER BY qid ASC')
        WordsChallenge = cursor.fetchall()
        query = "INSERT INTO Ranking (email, score, date) VALUES (%s, %s, %s)"
        for key in answer:
            if WordsChallenge[i]['answer'] == answer[key]:
                count = count + 1
                i = i + 1
            else:
                qnum.append(WordsChallenge[i]['qid'])
                q.append(WordsChallenge[i]['question'])
                rightans.append(WordsChallenge[i]['answer'])
                wrongans.append(answer[key])
                i = i + 1
        correction = dict(zip(qnum, zip(q, rightans, wrongans)))
        cursor.execute(query, (email, count, timestamp))
        mysql.connection.commit()
        # session["score"] = count
        return render_template("./html/wcresult.html", count = count, correction = correction, loginAccount=loginAccount)
    else:
        loginAccount = None
        return redirect('/signin')

@app.route("/wcrank", methods=['GET', 'POST'])
def rank():
    if session.get('loginAccount'):
        loginAccount = session['loginAccount']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Ranking ORDER BY score DESC')
        rank = cursor.fetchall()
        return render_template("./html/rank.html", loginAccount = loginAccount, rank = rank)
    else:
        loginAccount = None
        return redirect('/signin')

@app.route("/squiz", methods = ['GET'])
def squiz():
    if session.get('loginAccount'):
        email = session['loginAccount']['email']
        loginAccount = session['loginAccount']
        query = "SELECT * FROM packages WHERE email = %s"
        if request.method == 'GET':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query, (email,))
            packages = cursor.fetchall()
            num = len(packages)
            return render_template("./html/squiz.html", list=packages, loginAccount=loginAccount, num = num)
    else:
        loginAccount = None
        return redirect('/signin')

    
@app.route("/quiz", methods = ['GET', 'POST'])
def quiz():
    if session.get('loginAccount'):
        try:
            email = session['loginAccount']['email']
            loginAccount = session['loginAccount']
            i = 0
            j = 0
            k = 0
            nums = []
            name = []
            meaning = []
            alist = []
            query = "DELETE FROM Quiz WHERE qid > 0 AND email = %s"
            packid = request.form['id']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM sets')
            sets = cursor.fetchall()
            cursor.execute('SELECT * FROM words')
            words = cursor.fetchall()
            cursor.execute(query, (email,))
            mysql.connection.commit()

            for i in sets:
                if str(i['p_id']) == packid:
                    nums.append(i['w_id'])
            for j in words:
                for k in range(len(nums)):
                    if j['id'] == nums[k]:
                        name.append(j['name'])
                        meaning.append(j['meaning'])
            
            zip_iterator = zip(name, meaning)
            quizdict = dict(zip_iterator)

            for m, n in quizdict.items():
                for a in quizdict.keys():
                    alist.append(a)
                random.shuffle(alist)
                for x in alist[0:4]:
                    if x is m:
                        break
                else:
                    alist[random.randint(0,3)] = m
                cursor.execute('ALTER TABLE Quiz AUTO_INCREMENT=1')
                cursor.execute('INSERT INTO Quiz (email, problem, option1, option2, option3, option4, answer) VALUES (%s, %s, %s, %s, %s, %s, %s)', (email, n, alist[0], alist[1], alist[2], alist[3], m))
                mysql.connection.commit()
                alist.clear()
            query2 = "SELECT * FROM Quiz WHERE email = %s"
            cursor.execute(query2, (email,))

            quizset = cursor.fetchall()

            return render_template("./html/quiz.html", quizset = quizset, loginAccount=loginAccount)
        except:
            flash("You should have at least 4 cards in the package.")
            return redirect('./cardHome')
    else:
        loginAccount = None
        return redirect('/signin')

@app.route("/quizr", methods = ['GET', 'POST', 'DELETE'])
def qresult():
    if session.get('loginAccount'):
        email = session['loginAccount']['email']
        loginAccount = session['loginAccount']
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        i = 0
        count = 0
        qnum = []
        q = []
        rightans = []
        wrongans = []
        answer = request.form.to_dict()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query2 = "SELECT * FROM Quiz WHERE email = %s"
        cursor.execute(query2, (email,))
        quizset = cursor.fetchall()
        query = "INSERT INTO History (email, score, question, rightans, wrongans, date) VALUES (%s, %s, %s, %s, %s, %s)"
        for key in answer:
            if quizset[i]['answer'] == answer[key]:
                count = count + 1
                i = i + 1
            else:
                qnum.append(quizset[i]['qid'])
                q.append(quizset[i]['problem'])
                rightans.append(quizset[i]['answer'])
                wrongans.append(answer[key])
                i = i + 1
                
        for y in range(len(q)):
            cursor.execute(query, (email, count, q[y], rightans[y], wrongans[y], timestamp))
            mysql.connection.commit()
        correction = dict(zip(qnum, zip(q, rightans, wrongans)))
        return render_template("./html/quizr.html", count = count, correction = correction, loginAccount=loginAccount)
    else:
        loginAccount = None
        return redirect('/signin')

@app.route("/wceditor", methods = ['GET'])
def editor():
    if session.get('loginAccount'):
        loginAccount = session['loginAccount']
        isAdmin = session['loginAccount']['isAdmin']
        if isAdmin == 1:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM WordsChallenge ORDER BY qid ASC')
            wc = cursor.fetchall()
            return render_template("./html/wceditor.html", wc = wc, loginAccount=loginAccount)
        else:
            return redirect('/')
    else:
        loginAccount = None
        isAdmin = None
        return redirect('/signin')

@app.route("/addconfirm", methods = ['GET', 'POST', 'DELETE'])
def add():
    if session.get('loginAccount'):
        loginAccount = session['loginAccount']
    else:
        loginAccount = None
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    qid = request.form['qid']
    question = request.form['question']
    option1 = request.form['option1']
    option2 = request.form['option2']
    option3 = request.form['option3']
    option4 = request.form['option4']
    answer = request.form['answer']
    cursor.execute('INSERT INTO WordsChallenge (qid, question, option1, option2, option3, option4, answer) VALUES (%s, %s, %s, %s, %s, %s, %s)', (qid, question, option1, option2, option3, option4, answer))
    mysql.connection.commit()
    cursor.execute('SELECT * FROM WordsChallenge ORDER BY qid ASC')
    wc = cursor.fetchall()
    return render_template("./html/wceditor.html", wc = wc, loginAccount = loginAccount)

@app.route("/edit", methods = ['GET', 'POST', 'DELETE'])
def delete():
    if session.get('loginAccount'):
        loginAccount = session['loginAccount']
    else:
        loginAccount = None
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    q = request.form.to_dict()
    a = q["ans"]
    query = "DELETE FROM WordsChallenge WHERE answer = %s"
    if request.method == "POST":
        if request.form['submit_but'] == 'delete':
            cursor.execute(query, (a,))
            mysql.connection.commit()
    cursor.execute('ALTER TABLE WordsChallenge AUTO_INCREMENT=1')
    cursor.execute('SELECT * FROM WordsChallenge ORDER BY qid ASC')
    wc = cursor.fetchall()
    return render_template("./html/wceditor.html", wc = wc, q=q, a=a, loginAccount=loginAccount)

@app.route("/history", methods = ['GET'])
def history():
    if session.get('loginAccount'):
        email = session['loginAccount']['email']
        loginAccount = session['loginAccount']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT DISTINCT date FROM History WHERE email = %s ORDER BY date DESC"
        cursor.execute(query, (email, ))
        history_date = cursor.fetchall()
        return render_template("./html/history.html", loginAccount = loginAccount, date = history_date)
    else:
        loginAccount = None
        return redirect('/signin')

@app.route("/hisresult", methods = ['GET', 'POST'])
def hisresult():
    if session.get('loginAccount'):
        email = session['loginAccount']['email']
        loginAccount = session['loginAccount']
        date = request.form['date']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT * FROM History WHERE date = %s AND email = %s ORDER BY date DESC"
        print(query)
        cursor.execute(query, (date, email, ))
        history = cursor.fetchall()
        query2 = "SELECT DISTINCT date FROM History WHERE email = %s ORDER BY date DESC"
        cursor.execute(query2, (email, ))
        history_date = cursor.fetchall()
        return render_template("./html/history.html", loginAccount = loginAccount, his = history, date = history_date)
    else:
        loginAccount = None
        return redirect('/signin')

# NOTECARD 
def addWordToPackage(pName, wName):
    email = session['loginAccount']['email']
    connection = mysql.connection
    cursor = connection.cursor()
    cursor.execute(
        f"""select id from packages where email = '{email}' and name = '{pName}';""")

    p_id = cursor.fetchall()[0][0]
    cursor.execute(
        f"""select id from words where email = '{email}' and name = '{wName}';""")
    w_id = cursor.fetchall()[-1][0]
    cursor.execute(
        f"""insert into sets (email, p_id, w_id) values ('{email}',{p_id}, {w_id});""")
    connection.commit()
    cursor.close()

# Method for a notecard containing


def addWord(word, image='', pos='', definition=''):
    email = session['loginAccount']['email']
    definition = definition.strip().replace('.\n', '.|')

    sql = f"""insert into words (email, name, pos, meaning, image) values ('{email}','{word}', '{pos}', "{definition}", '{image}')"""
    connection = mysql.connection
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    cursor.close()

# Edit a card in showCard


def updateWord(id, word, image='', pos='', definition=''):
    email = session['loginAccount']['email']
    definition = definition.strip().replace('.\n', '.|')
    sql = f"""update words set name='{word}', pos='{pos}', meaning="{definition}", image='{image}' where email = '{email}' and id = {id}"""
    connection = mysql.connection
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    cursor.close()

# deleting card in the corresponding package


def deleteWordFromPackage(pIndex, wIndex):
    email = session['loginAccount']['email']
    connection = mysql.connection
    cursor = connection.cursor()
    cursor.execute(
        f"""delete from sets where email = '{email}' and p_id = '{pIndex}' and w_id = '{wIndex}';""")
    connection.commit()
    cursor.close()

# deleting a card itself.


def deleteWord(wIndex):
    email = session['loginAccount']['email']
    connection = mysql.connection
    cursor = connection.cursor()
    cursor.execute(
        f"""delete from words where email = '{email}' and id = '{wIndex}';""")
    connection.commit()
    cursor.close()

# deleting a package itself


def deletePack(pIndex):
    email = session['loginAccount']['email']
    connection = mysql.connection
    cursor = connection.cursor()
    cursor.execute(
        f"""delete from packages where email = '{email}' and id = '{pIndex}';"""
    )
    connection.commit()
    cursor.close()

# deleting all cards in the corresponding package


def deleteWordsInPackage(pIndex):
    email = session['loginAccount']['email']
    connection = mysql.connection
    cursor = connection.cursor()
    cursor.execute(
        f"""delete from sets where email = '{email}' and p_id = '{pIndex}';""")
    connection.commit()
    cursor.close()


def getPackageList():
    email = session['loginAccount']['email']
    package_list = []
    connection = mysql.connection
    cursor = connection.cursor()

    cursor.execute(f'''select p.id, p.name, w_id, w.name from sets s 
                            right join packages p on s.p_id = p.id
                            left join words w on s.w_id = w.id
                            WHERE p.email='{email}';''')
    result = cursor.fetchall()
    for row in result:
        isExist = False
        word = {'id': row[2], 'name': row[3]}
        for package in package_list:
            if package['id'] == row[0]:
                package['words'].append(word)
                isExist = True
                break
        if not isExist:
            package_list.append(
                {'id': row[0], 'name': row[1], 'words': [word]})
    cursor.close()
    return package_list


def getWord(w_id):
    email = session['loginAccount']['email']
    cursor = mysql.connection.cursor()
    cursor.execute(
        f"""select * from words WHERE email = '{email}' and id='{w_id}' ;""")
    result = cursor.fetchall()
    cursor.close()
    return {
        'name': result[0][2],
        'pos': result[0][3],
        'meaning': result[0][4].split('|'),
        'image': result[0][5]
    }

# Bring search history db order of descending search date record.


def getSearchHistory():
    email = session['loginAccount']['email']
    cursor = mysql.connection.cursor()
    cursor.execute(
        f"""SELECT word FROM HasSearchHistory WHERE email = '{email}' order by regDate desc;""")
    result = cursor.fetchall()
    cursor.close()
    return [his[0] for his in result]


@ app.route('/cardHome', methods=['GET', 'POST'])
def cardHome():
    if session.get('loginAccount') == None:

        return redirect('/signin')
    else:
        email = session['loginAccount']['email']
        loginAccount = session['loginAccount']
        # POST 일때 (=Add New Package)
        if request.method == 'POST':
            connection = mysql.connection
            cursor = connection.cursor()
            value = request.form.get('newPackage')
            if value != '':
                sql = f"insert into packages (email, name) values ('{email}', '{value}');"
                cursor.execute(sql)
                connection.commit()
            cursor.close()

        return render_template('html/cardHome.html', packages=getPackageList(), loginAccount=loginAccount)


@ app.route('/makeCard', methods=['GET', 'POST', 'PUT'])
def makeCard():
    if session.get('loginAccount'):
        loginAccount = session['loginAccount']
        if request.method == 'POST':
            data = request.get_json()
            package = data['package']
            image = data['image']
            word = data['word']
            pos = data['pos']
            definition = data['definition']
            if package and word:
                addWord(word, image, pos, definition)
                addWordToPackage(package, word)
                return jsonify(result='success')
            else:
                return jsonify(result='failed')
        if request.method == 'PUT':
            data = request.get_json()
            id = data['id']
            image = data['image']
            word = data['word']
            pos = data['pos']
            definition = data['definition']
            if id and word:
                updateWord(id, word, image, pos, definition)
                return jsonify(result='success')
            else:
                return jsonify(result='failed')

        return render_template('html/makeCard.html', packages=getPackageList(), history=getSearchHistory(), loginAccount=loginAccount)
    else:
        return 'fail'


@ app.route('/showCard', methods=['GET', 'POST'])
def showCard():
    if session.get('loginAccount'):
        loginAccount = session['loginAccount']
        if request.method == 'GET':
            param_dict = request.args.to_dict()
            package_list = getPackageList()
            p_id = int(
                param_dict['package']) if 'package' in param_dict else package_list[0]['id']
            p_in_p = 0
            for p_i in range(len(package_list)):
                if package_list[p_i]['id'] == p_id:
                    p_in_p = p_i
                    break
        # w_id = int(
            # param_dict['word']) if 'word' in param_dict else package_list[p_in_p]['words'][0]['id']
            w_id = 0
            if 'word' in param_dict:
                value = param_dict['word']
                if value == None or value == 'None':
                    w_id = package_list[p_in_p]['words'][0]['id']
                else:
                    w_id = int(value)
            else:
                w_id = package_list[p_in_p]['words'][0]['id']
            w_in_p = 0
            for w_i in range(len(package_list[p_in_p]['words'])):
                if package_list[p_in_p]['words'][w_i]['id'] == w_id:
                    w_in_p = w_i
                    break
            try:
                word = getWord(w_id)
            except IndexError:
                word = {'name': 'None', 'pos': 'None', 'meaning': ['None']}

        return render_template('html/showCard.html', loginAccount=loginAccount, packages=package_list, p_index=p_id, p_in_p=p_in_p, w_index=w_id, w_in_p=w_in_p, word=word)
    else:
        return 'fail'


@app.route('/deletePackage')
def deletePackage():
    if session.get('loginAccount'):
        param_dict = request.args.to_dict()
        p_str = param_dict['package'] if 'package' in param_dict else ''
        if p_str != '':
            p_list = p_str.split(',')
            for p in p_list:
                deleteWordsInPackage(int(p))
                deletePack(int(p))
        return redirect('/cardHome')
    else:
        return 'fail'


@ app.route('/deleteCard')
def deleteCard():
    if session.get('loginAccount'):
        param_dict = request.args.to_dict()
        p_index = int(param_dict['package']) if 'package' in param_dict else 0
        w_index = int(param_dict['word']) if 'word' in param_dict else 0
        deleteWordFromPackage(p_index, w_index)
        deleteWord(w_index)
        return redirect('/showCard?package='+str(p_index))
    else:
        return 'fail'


@ app.route('/addPackage', methods=['POST'])
def addPackage():
    if session.get('loginAccount'):
        email = session['loginAccount']['email']
        data = request.get_json()
        exist = data['exist']
        name = data['name']
        words = data['words']

        if not exist:
            connection = mysql.connection
            cursor = connection.cursor()
            cursor.execute(
                f"insert into packages (email, name) values ('{email}', '{name}');")
            connection.commit()
            cursor.close()

        for word in words:
            addWord(word)
            addWordToPackage(name, word)

        return 'cardHome'
    else:
        return 'fail'
    

if __name__ == '__main__':
    app.secret_key = '0000'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host="0.0.0.0", port=5000)