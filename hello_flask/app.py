from flask import Flask,render_template,request
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

from datetime import date
import bcrypt

import riotgames

from db_con import get_db_instance, get_db

app = Flask(__name__)
FlaskJSON(app)

USER_PASSWORDS = { "cjardin": "strong password"}

IMGS_URL = {
            "DEV" : "/static",
            "INT" : "https://cis-444-fall-2021.s3.us-west-2.amazonaws.com/images",
            "PRD" : "http://d2cbuxq67vowa3.cloudfront.net/images"
            }

CUR_ENV = "PRD"
JWT_SECRET = None

global_db_con = get_db()


with open("secret", "r") as f:
    JWT_SECRET = f.read()

@app.route('/') #endpoint
def index():
    return 'Web App with Python Caprice!' + USER_PASSWORDS['cjardin']

@app.route('/buy') #endpoint
def buy():
    return 'Buy'

@app.route('/hello') #endpoint
def hello():
    return render_template('hello.html',img_url=IMGS_URL[CUR_ENV] )


@app.route('/back',  methods=['GET']) #endpoint
def back():
    return render_template('backatu.html',input_from_browser=request.args.get('usay', default = "nothing", type = str) )

@app.route('/backp',  methods=['POST']) #endpoint
def backp():
    print(request.form)
    salted = bcrypt.hashpw( bytes(request.form['fname'],  'utf-8' ) , bcrypt.gensalt(10))
    print(salted)

    print(  bcrypt.checkpw(  bytes(request.form['fname'],  'utf-8' )  , salted ))

    return render_template('backatu.html',input_from_browser= str(request.form) )

@app.route('/auth',  methods=['POST']) #endpoint
def auth():
        print(request.form)
        return json_response(data=request.form)



#Assigment 2
@app.route('/ss1') #endpoint
def ss1():
    return render_template('server_time.html', server_time= str(datetime.datetime.now()) )

@app.route('/getTime') #endpoint
def get_time():
    return json_response(data={"password" : request.args.get('password'),
                                "class" : "cis44",
                                "serverTime":str(datetime.datetime.now())
                            }
                )

@app.route('/auth2') #endpoint
def auth2():
    jwt_str = jwt.encode({"username" : "cary",
                            "age" : "so young",
                            "books_ordered" : ['f', 'e'] }
                            , JWT_SECRET, algorithm="HS256")
    #print(request.form['username'])
    return json_response(jwt=jwt_str)

@app.route('/exposejwt') #endpoint
def exposejwt():
    jwt_token = request.args.get('jwt')
    print(jwt_token)
    return json_response(output=jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"]))


@app.route('/hellodb') #endpoint
def hellodb():
    cur = global_db_con.cursor()
    cur.execute("insert into music values( 'dsjfkjdkf', 1);")
    global_db_con.commit()
    return json_response(status="good")


#Assignment 3
@app.route('/authUser', methods=['POST'])#endpoint
def authUser():
    print(request.form)
    print('=============')

    cur = global_db_con.cursor()

    uName = "SELECT password FROM users WHERE username ='"
    uName += request.form['uname']
    uName += "';"

    cur.execute(uName)

    x = cur.fetchone()

    print (x[0])

    credentials = str(x[0])
    if bcrypt.checkpw(bytes(request.form['pword'], 'utf-8'),credentials.encode('utf-8')):
        jwt_str = jwt.encode({"username": request.form['uname'], "password": request.form['pword']}, JWT_SECRET, algorithm='HS256')

        print('=========')
        print(jwt_str)

        return json_response(jwt=jwt_str)

    print('Invalid')

    return json_response(status='401',msg="Invalid Credentials")

@app.route('/newUser', methods=['POST']) #endpoint
def newUser():
    print(request.form)

    tempU = request.form['newUser']
    tempP = request.form['newPass']

    saltyBoi = bcrypt.hashpw(bytes(request.form['newPass'], 'utf-8'), bcrypt.gensalt(10))

    print(tempU)
    print(saltyBoi.decode('utf-8'))

    sub = "INSERT INTO users (username, password) VALUES ('"
    sub += str(tempU)
    sub += "','"
    sub += str(saltyBoi.decode('utf-8'))
    sub += "');"

    print(sub)

    cur = global_db_con.cursor()
    cur.execute(sub)
    global_db_con.commit()

    return json_response(status="good")

@app.route('/getBooks', methods=['GET']) #endpoint
def getBooks():
    print('Verifying JWT')

    authHeader = request.headers.get('Authorization')

    print(authHeader)

    tokenVal = checkToken(authHeader)

    print('============')
    #print(decoded.get('username'))
    #print('============')
    #print(decoded.get('password'))

    if tokenVal == False:
        return json_response(status='404', msg='Invalid JWT Token')

    print('JWT Valid')

    cur = global_db_con.cursor()
    book_titleReq = 'SELECT title FROM books;'
    cur.execute(book_titleReq)
    book_titleResp = cur.fetchall()

    print(book_titleResp)

    book_priceReq = 'SELECT price FROM books;'
    cur.execute(book_priceReq)
    book_priceResp = cur.fetchall()

    print(book_priceResp)

    return json_response(jwt=authHeader, bookTitles=book_titleResp, bookPrices=book_priceResp)

@app.route('/buyBook', methods=['POST']) #endpoint
def buyBook():

    authHeader = request.headers.get('Authorization')

    tokenVal = decodeToken(authHeader)

    print(tokenVal)

    book = request.form['Book']

    print(book)

    today = date.today()

    print(today)

    cart = "INSERT INTO cart (username, title, dop) VALUES ('"
    cart += str(tokenVal)
    cart += "','"
    cart += str(book)
    cart += "','"
    cart += str(today)
    cart += "');"

    print(cart)

    cur = global_db_con.cursor()
    cur.execute(cart)
    global_db_con.commit()

    return json_response(status="good")


def decodeToken(token):
    print('in decode token')

    decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    tStr = decoded.get('username')

    return tStr

def checkToken(token):
    print(token)
    print('in check token')


    tStr = decodeToken(token)
    cur = global_db_con.cursor()

    print(tStr)

    dbUser = "SELECT EXISTS (SELECT username FROM users WHERE username ='"
    dbUser += tStr
    dbUser += "' LIMIT 1);"

    print(dbUser)

    cur.execute(dbUser)
    x = cur.fetchone()

    print('x is ')
    print(x[0])

    if x[0]:
        print('token valid')
        return True
    else:
        print('token invalid')
        return False

#finalassignment


@app.route('/populateTable', methods=['GET']) #endpoint
def populateTable():

    print(request.args)

    sumName = request.args['sName']

    print(sumName)

    returns = riotgames.summonerInfo(sumName)
    print(returns['name'])

    return json_response(returns)

app.run(host='0.0.0.0', port=80)
