from flask import Flask, render_template, redirect, session, flash, request
from mysqlconnection import MySQLConnector
import re
import md5
import os
import binascii
app = Flask(__name__)
app.secret_key = 'wn2!f2nCch2cp@2238h23b233p2SVW12n9df'

# Connects Application and the database
mysql = MySQLConnector(app, 'walldb')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Login Page
@app.route('/')
def index():
    return render_template('index.html')

# The Wall
@app.route('/wall')
def wall():
    if 'user' not in session:
        flash('You must be logged in to see the wall')
        return redirect('/')

    posts = ''

    # Gather all messages from messages table
    query = 'SELECT messages.id, first_name, last_name, message, messages.created_at FROM messages LEFT JOIN users ON users.id = messages.users_id ORDER BY messages.id ASC;'
    messages = mysql.query_db(query)
    
    
    # Display all messages with names and date when the message was created.
    for message in messages:
        # Gather all names linked to messages
        message_id = message['id']
        print message_id
        posts += '<div class="bold">'+message['first_name']+' ' +message['last_name']+' - '+str(message['created_at'])+'</div>'
        posts += '<div class="moveover">'+message['message']+'</div>'
        
        query = 'SELECT comments.id, messages_id, first_name, last_name, comment, comments.created_at FROM comments LEFT JOIN users ON users.id = comments.users_id WHERE comments.messages_id ='+str(message_id)+' ORDER BY comments.id;'
        comments = mysql.query_db(query)
        print comments
        # Loop through all comments for each message
        if comments != []:
            for comment in comments:
                if comment['messages_id'] == message_id:
                    posts += '<div class="moveovermore">'+comment['first_name']+' ' + comment['last_name']+' - '+str(comment['created_at'])+'</div>'
                    posts += '<div class="comment">'+comment['comment']+'</div>'
        posts += '<br><h3>Post a comment</h3><form action="/'+str(message_id)+'/comment" method="POST"><textarea name="comment" id="boxy" cols="80" rows="4"></textarea><br><br><input type="submit" value="Post a comment"></form><br>'
        
    return render_template('wall.html', posts=posts)


# Process/Verify registration
@app.route('/register', methods=['POST'])
def register():
    # Gather information from form
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    # print first_name, last_name, email, password, confirm_password

    # Form Validations

    # First Name Validations
    if first_name == '':
        flash('First name can not be blank')
        return redirect('/')
    elif not first_name.isalpha():
        flash('First Name must not contain numbers')
        return redirect('/')
    elif len(first_name) < 2:
        flash('First Name must be longer than 2 characters')
        return redirect('/')

    # Last Name Validations
    if last_name == '':
        flash('Last name can not be blank')
        return redirect('/')
    if not last_name.isalpha():
        flash('Last Name must not contain numbers')
        return redirect('/')
    elif len(last_name) < 2:
        flash('Last Name must be longer than 2 characters')
        return redirect('/')

    # Email Validations
    if email == '':
        flash('Email can not be blank')
        return redirect('/')
    elif not EMAIL_REGEX.match(email):
        flash('Email is not in a valid format')
        return redirect('/')

    # Password Validations
    if password == '':
        flash('Password can not be blank')
        return redirect('/')
    elif len(password) < 8:
        flash('Password must be atleast 8 characters')
        return redirect('/')

    # Confirm Password Validations
    if not confirm_password == password:
        flash('Password and Confirm Password do not match')
        return redirect('/')

    # Insert Validated User into database
    salt = binascii.b2a_hex(os.urandom(15))
    hashed_password = md5.new(password+salt).hexdigest()
    query = 'INSERT INTO users (first_name, last_name, email, password, salt, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, :salt, now(), now());'
    data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': hashed_password,
        'salt': salt
    }
    mysql.query_db(query, data)

    return redirect('/wall')

# Process/Verify Login
@app.route('/login', methods=['POST'])
def login():
    # Gather data from form
    email = request.form['email']
    password = request.form['password']

    # Make sure input fields are not empty
    if email == '':
        flash('Email field is empty')
        return redirect('/')
    if password == '':
        flash('Password field is empty')
        return redirect('/')

    # Search/Select User in database that matches inputted email
    query = 'SELECT * FROM users WHERE email = :email LIMIT 1;'
    data = {
        'email': email
    }
    user = mysql.query_db(query, data)

    # Confirm password entered is correct
    if not user == []:
        encrypted_password = md5.new(password+user[0]['salt']).hexdigest()
        if user[0]['password'] == encrypted_password:
            # If correct, send to The Wall
            # Link Name of User to all messages and comments
            if 'user' not in session:
                session['user'] = user
            return redirect('/wall')
        else:
            flash('Invalid email or password')
            # If invalid send back to login page
            return redirect('/')
    else:
        flash('Invalid email or password')
        # If invalid send back to login page
        return redirect('/')
    return redirect('/')

# Insert messages into db linked to specific users
@app.route('/message', methods=['POST'])
def message():
    user = session['user']
    message = request.form['message']
    # # Insert new message into database
    query = 'INSERT INTO messages (users_id, message, created_at, updated_at) VALUES (:users_id, :message, now(), now());'
    data = {
        'users_id': user[0]['id'],
        'message': message
    }
    mysql.query_db(query, data)

    return redirect('/wall')

# Insert comments into db linked to their specific messages
@app.route('/<message_id>/comment', methods=['POST'])
def comment(message_id):
    user = session['user']
    comment = request.form['comment']
    # # Insert new message into database
    query = 'INSERT INTO comments (messages_id, users_id, comment, created_at, updated_at) VALUES (:messages_id, :users_id, :comment, now(), now());'
    data = {
        'messages_id': message_id,
        'users_id': user[0]['id'],
        'comment': comment
    }
    mysql.query_db(query, data)
    return redirect('/wall')


# Log out current user
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


app.run(debug=True)
