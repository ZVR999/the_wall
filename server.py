from flask import Flask, render_template, redirect, session, flash, request
from mysqlconnection import MySQLConnector
import re, md5, os, binascii 
app = Flask(__name__)
app.secret_key = 'wn2!f2nCch2cp@2238h23b233p2SVW12n9df'

# Connects Application and the database 
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

# Login Page 
@app.route('/')
def index():
    return render_template('index.html')

# The Wall
@app.route('/wall')
def wall():    
    return render_template('wall.html')

# Process/Verify registration
@app.route('/register', methods=['POST'])
def register():    
    # Gather information from form
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    print first_name, last_name, email, password, confirm_password

    # Form Validations 
    
    #First Name Validations 
    # if first_name == '':
    #     flash('First name can not be blank')
    #     return redirect('/') 
    # elif not first_name.isalpha():
    #     flash('First Name must not contain numbers')
    #     return redirect('/')
    # elif len(first_name) < 2:
    #     flash('First Name must be longer than 2 characters')
    #     return redirect('/')
    
    # #Last Name Validations
    # if last_name == '':
    #     flash('Last name can not be blank')
    #     return redirect('/')
    # if not last_name.isalpha():
    #     flash('Last Name must not contain numbers')
    #     return redirect('/')
    # elif len(last_name) < 2:
    #     flash('Last Name must be longer than 2 characters')
    #     return redirect('/')

    # Email Validations
    # if email == '':
    #     flash('Email can not be blank')
    #     return redirect('/')
    # elif not EMAIL_REGEX.match(email):
    #     flash('Email is not in a valid format')
    #     return redirect('/')

    # Password Validations
    # if password == '':
    #     flash('Password can not be blank')
    #     return redirect('/')
    # elif len(password) < 8:
    #     flash('Password must be atleast 8 characters')
    #     return redirect('/')

    # Confirm Password Validations
    # if not confirm_password == password:
    #     flash('Password and Confirm Password do not match')
    #     return redirect('/')

    # Insert Validated User into database
    query = 'SELECT * FROM users;'
    print mysql.query_db(query)

    return redirect('/')

# Process/Verify Login
@app.route('/login', methods=['POST'])
def login():
    return redirect('/wall')

app.run(debug=True)