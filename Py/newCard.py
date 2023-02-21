from flask import Flask, render_template, request, jsonify, redirect
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='../static')
app._static_folder = '../static'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '0000'
app.config['MYSQL_DB'] = 'cse416'

mysql = MySQL(app)


def addWordToPackage(pName, wName):
    connection = mysql.connection
    cursor = connection.cursor()
    cursor.execute(f"""select id from packages where name = '{pName}';""")
    p_id = cursor.fetchall()[0][0]
    cursor.execute(f"""select id from words where name = '{wName}';""")
    w_id = cursor.fetchall()[0][0]
    cursor.execute(f"""insert into sets values ({p_id}, {w_id});""")
    connection.commit()
    cursor.close()


def addWord(word, image='', pos='', definition=''):
    definition = definition.strip().replace('.\n', '.|')
    sql = f"""insert into words (name, pos, meaning, image) values 
        ('{word}', '{pos}', "{definition}", '{image}')"""
    connection = mysql.connection
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    cursor.close()


def updateWord(id, word, image='', pos='', definition=''):
    definition = definition.strip().replace('.\n', '.|')
    sql = f"""update words set name='{word}', pos='{pos}', meaning="{definition}", image='{image}' where id = {id}"""
    connection = mysql.connection
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    cursor.close()


def deleteWordFromPackage(pIndex, wIndex):
    connection = mysql.connection
    cursor = connection.cursor()
    cursor.execute(
        f"""delete from sets where p_id = '{pIndex}' and w_id = '{wIndex}';""")
    connection.commit()
    cursor.close()


def deleteWord(wIndex):
    connection = mysql.connection
    cursor = connection.cursor()
    cursor.execute(f"""delete from words where id = '{wIndex}';""")
    connection.commit()
    cursor.close()


def getPackageList():
    package_list = []
    connection = mysql.connection
    cursor = connection.cursor()
    cursor.execute('''select p.id, p.name, w_id, w.name from sets s 
                            right join packages p on s.p_id = p.id 
                            left join words w on s.w_id = w.id;''')
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
    cursor = mysql.connection.cursor()
    cursor.execute(f"""select * from words where id='{w_id}';""")
    result = cursor.fetchall()
    cursor.close()
    return {
        'name': result[0][1],
        'pos': result[0][2],
        'meaning': result[0][3].split('|'),
        'image': result[0][4]
    }


def getSearchHistory():
    cursor = mysql.connection.cursor()
    cursor.execute(
        f"""SELECT * FROM HasSearchHistory order by regDate desc;""")
    result = cursor.fetchall()
    cursor.close()
    return [his[1] for his in result]


@app.route('/')
@app.route('/search')
def home():
    return render_template('html/search.html')


@app.route('/cardHome', methods=['GET', 'POST'])
def cardHome():
    # POST 일때 (=Add New Package)
    if request.method == 'POST':
        connection = mysql.connection
        cursor = connection.cursor()
        value = request.form.get('newPackage')
        sql = f"insert into packages (name) values ('{value}');"
        cursor.execute(sql)
        connection.commit()
        cursor.close()

    return render_template('html/cardHome.html', packages=getPackageList())


@app.route('/makeCard', methods=['GET', 'POST', 'PUT'])
def makeCard():
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

    return render_template('html/makeCard.html', packages=getPackageList(), history=getSearchHistory())


@app.route('/showCard', methods=['GET', 'POST'])
def showCard():
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

    return render_template('html/showCard.html', packages=package_list, p_index=p_id, p_in_p=p_in_p, w_index=w_id, w_in_p=w_in_p, word=word)


@app.route('/showCard2')
def showCard2():
    return render_template('showCard2.html')


@app.route('/deleteCard')
def deleteCard():
    param_dict = request.args.to_dict()
    p_index = int(param_dict['package']) if 'package' in param_dict else 0
    w_index = int(param_dict['word']) if 'word' in param_dict else 0
    deleteWordFromPackage(p_index, w_index)
    deleteWord(w_index)
    return redirect('/showCard?package='+str(p_index))


@app.route('/addScHis', methods=['POST'])
def addScHis():
    word = request.data.decode()
    cursor = mysql.connection.cursor()
    cursor.execute(
        f"INSERT INTO  HasSearchHistory (word,regDate) VALUES ('{word}',SYSDATE())")
    mysql.connection.commit()
    cursor.close()
    return 'ok'


@app.route('/addPackage', methods=['POST'])
def addPackage():
    connection = mysql.connection
    cursor = connection.cursor()

    data = request.get_json()
    name = data['name']
    cursor.execute(f"insert into packages (name) values ('{name}');")
    connection.commit()
    cursor.close()

    words = data['words']
    for word in words:
        addWord(word)
        addWordToPackage(name, word)

    return 'cardHome'


app.run(debug=True)

