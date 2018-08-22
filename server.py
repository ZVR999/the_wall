from flask import Flask, render_template, redirect, session, flash, request
from mysqlconnection import MySQLConnector
import re, md5, os, binascii 
app = Flask(__name__)
app.secret_key = 'wn2!f2nCch2cp@2238h23b233p2SVW12n9df'

mysql = MySQLConnector(app,'walldb')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    # RETRIEVE PASSWORD WHEN LOGGING IN
    # salt =  binascii.b2a_hex(os.urandom(15))
    # hashed_password = md5.new(password + salt).hexdigest()
    # user_query = "SELECT * FROM users WHERE users.email = :email LIMIT 1"
    # query_data = {'email': email}
    # user = mysql.query_db(user_query, query_data)
    
    # if len(user) != 0:
    #     encrypted_password = md5.new(password + user[0]['salt']).hexdigest()
    # if user[0]['password'] == encrypted_password:
    #     session['logged_in'] = 1
    #     return redirect('/success')
    # else:
    #     flash('Invalid email or password')
    #     return redirect('/')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wall')
def wall():    
    return render_template('wall.html')

@app.route('/register', methods=['POST'])
def register():    

    return redirect('/wall')

@app.route('/login', methods=['POST'])
def login():
    return redirect('/wall')

app.run(debug=True)