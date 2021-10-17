#!/usr/local/bin/python

#Paul Wasilewicz
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import timedelta
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import os
import MySQLdb
import MySQLdb.cursors
import requests
import base64
import json

#apiKey =

app = Flask(__name__, static_url_path='')
#app.debug = True
app.secret_key = os.urandom(16)


app.config.update(
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_HTTPONLY=False,
    SESSION_COOKIE_SAMESITE='Lax',
)

def get_db(): #enter MySQL login
    db = MySQLdb.connect(
        host="",
        user="",
        passwd="",
    )

    return db

def createDB():
    cursor = get_db().cursor()
    cursor.execute("SHOW DATABASES")
    flag = 0

    for i in cursor:
        if str(i) == '(\'wasilewp\',)':
            flag = 1
            cursor.execute("USE wasilewp")
            cursor.execute("SHOW TABLES")
            if cursor.rowcount == 0:
                    cursor.execute("CREATE TABLE users (name VARCHAR(255), password VARCHAR(255));")
            break

    if flag == 0:
        cursor.execute("CREATE DATABASE wasilewp")
        cursor.execute("USE wasilewp")
        cursor.execute("CREATE TABLE users (name VARCHAR(255), password VARCHAR(255));")


@app.route('/')
def index(name=None):
    #if 'username' in session:
        #display the welcome user page
        #return 'Logged in as %s' % escape(session['username'])
    #return 'You are not logged in'
    #else display the login page
    return render_template('coinBaseTemplate.html', name=name)


@app.route('/coinBaseSearch', methods=['POST'])
def coinBaseSearch():

    crypto = request.get_json()
    cryptoList = ["BTC","ETH","USDT","XRP","BCH","LINK","BNB","LTC","DOT","ADA"]
    if crypto['cur'] == 'top10':
        cryptoDict = {}
        for i in cryptoList:
            spot = "https://api.coinbase.com/v2/prices/"+i+"-CAD/spot"
            buy = "https://api.coinbase.com/v2/prices/"+i+"-CAD/buy"
            sell = "https://api.coinbase.com/v2/prices/"+i+"-CAD/sell"




    reqStringSpot = "https://api.coinbase.com/v2/prices/"+crypto['cur']+"-CAD/spot"
    reqStringBuy = "https://api.coinbase.com/v2/prices/"+crypto['cur']+"-CAD/buy"
    reqStringSell = "https://api.coinbase.com/v2/prices/"+crypto['cur']+"-CAD/sell"


    responseSpot = requests.get(reqStringSpot)
    responseBuy = requests.get(reqStringBuy)
    responseSell = requests.get(reqStringSell)
    #response = requests.get("https://api.coinbase.com/v2/prices/spot?currency=CAD")
    #print(response.status_code,type(response.status_code))
    if responseSpot.status_code == 200 and responseBuy.status_code == 200 and responseSell.status_code == 200:
        return jsonify(error='success', spotAns=responseSpot.json()['data']['amount'], base=responseSpot.json()['data']['base'], currency=responseSpot.json()['data']['currency'], buyAns=responseBuy.json()['data']['amount'], sellAns=responseSell.json()['data']['amount'])
    else:
        return jsonify(error='invalid')

@app.route('/coinMarketCap', methods=['POST'])
def coinMarketCap():
    apiKey = '' #enter api key

    crypto = request.get_json()
    try:
        numToFind = int(crypto['amount'])
    except:
        return jsonify(error='invalid')
    if numToFind > 2000:
        return jsonify(error='invalid')

    url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'1',
    'limit':str(numToFind),
    'convert':'USD'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    return json.dumps(data)

@app.route('/loginOrCreate', methods=['POST'])
def loginOrCreate():
    createDB()
    dataB = get_db()
    cursor = dataB.cursor()

    #print(session.get('username'))
    if request.is_json:
        if request.method == 'POST':
            #print('were about to check for existence')
            theUser = request.get_json()
            userName = theUser['uname']
            pwd = theUser['psw']
            cursor.execute("USE wasilewp")
            cursor.execute("SELECT name FROM users WHERE name LIKE"+'\''+userName+'\'')
            if cursor.rowcount == 1:
                #the user exists
                cursor.execute("SELECT name FROM users WHERE name LIKE \""+userName+"\" AND password LIKE \""+pwd+"\"")
                if cursor.rowcount == 1:
                    session['username'] = userName

                    return redirect(url_for("index"))
                else:
                    return jsonify(error='BadPass')
            else:
                #make the user
                cursor.execute("INSERT INTO users (name,password) VALUES (\""+userName+"\",\""+pwd+"\")")
                dataB.commit()

                session['username'] = userName
                session['flag'] = 0
                return redirect(url_for("index"))


    return


@app.route('/logout', methods=['POST'])
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

@app.route('/user',methods=['POST','DELETE','GET','PUT'])
def user():

    createDB()
    dataB = get_db()
    cursor = dataB.cursor()

    if request.is_json:
        if request.method == 'POST':
            print('create')
            theUser = request.get_json()
            userName = theUser['uname']
            pwd = theUser['psw']
            cursor.execute("USE wasilewp")
            cursor.execute("SELECT name FROM users WHERE name LIKE"+'\''+userName+'\'')

            if cursor.rowcount == 1:
                return jsonify(error='exists')
            else:
                query = "INSERT INTO users (name,password) VALUES (\""+userName+"\",\""+pwd+"\")"
                #val = (userName, pwd)
                cursor.execute(query)
                dataB.commit()
                return jsonify(error='success', usrn=userName)
        elif request.method == 'DELETE':
            print('del')
            theUser = request.get_json()
            userName = theUser['uname']
            pwd = theUser['psw']
            cursor.execute("USE wasilewp")
            cursor.execute("SELECT name FROM users WHERE name LIKE \""+userName+"\" AND password LIKE \""+pwd+"\"")

            if cursor.rowcount == 1:
                #delete
                query = "DELETE FROM users WHERE name LIKE \""+userName+"\" AND password LIKE \""+pwd+"\""
                cursor.execute(query)
                dataB.commit()
                return jsonify(error='success',usrn=userName)
            else:
                print('return invalid')
                return jsonify(error='invalid')
        elif request.method == 'PUT':
            print('update')
            theUser = request.get_json()
            print(theUser)
            userName = theUser['uname']
            pwd = theUser['psw']
            newPwd = theUser['newP']
            cursor.execute("USE wasilewp")
            cursor.execute("SELECT name FROM users WHERE name LIKE \""+userName+"\" AND password LIKE \""+pwd+"\"")
            if cursor.rowcount == 1:
                print("UPDATE users SET password=\'"+newPwd+"\' WHERE name=\'"+userName+"\';")
                cursor.execute("UPDATE users SET password=\'"+newPwd+"\' WHERE name=\'"+userName+"\';")
                dataB.commit()
                return jsonify(error='success',usrn=userName)
            else:
                return jsonify(error='invalid')

    if request.method == 'GET':
        userStr = ''
        passStr = ''
        cursor.execute("USE wasilewp")
        cursor.execute("SELECT * FROM users;")
        result = cursor.fetchall()

        for x in result:
            userStr = userStr+','+x[0]
            passStr = passStr+','+x[1]



        if cursor.rowcount > 0:
            return jsonify(users=userStr,passwords=passStr)
        else:
            return jsonify(error='invalid')


    return 'Fail'
