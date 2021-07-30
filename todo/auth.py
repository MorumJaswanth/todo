from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from . import db
from flask import g
from .models import User

auth = Blueprint('auth', 'auth',url_prefix="")

@auth.route('/login',methods=['GET'])
def login():
    
    print("Login")
    return render_template('login.html')

@auth.route('/signup')
def signup():

    print("Signup in get")
    return render_template('signup.html')


def userid(email):
    conn=db.get_db()
    cursor=conn.cursor()
    cursor.execute(f"select l.id from userlist l where email='{email}';")
    creds=cursor.fetchone()[0]
    return creds    
    
@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    conn=db.get_db()
    cursor=conn.cursor()
    cursor.execute(f"select l.email,l.pswrd,l.id from userlist l where email='{email}';")
    creds=cursor.fetchone()
    try:
        user=creds[0]
    except:
        user=False
    
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(creds[1],password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
    session.clear()
    
    user=User(creds[2])
    login_user(user,remember=remember,force=True)
    
    session["user_id"] = creds[2]
    #session["active"]=True
    return redirect(url_for('todo.dashboard'))
    #return (f"output is {user.id}")



@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    username = request.form.get('username')
    password = generate_password_hash(request.form.get('password'), method='sha256')

    conn=db.get_db()
    cursor=conn.cursor()
    cursor.execute(f"select l.email from userlist l where email='{email}';")
    try:
        user=cursor.fetchone()[0]
    except:
        user=False
    if user: 
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    cursor.execute(f"INSERT into userlist(name,username,email,pswrd) values ('{name}','{username}','{email}','{password}')")
    conn.commit()
    
    return redirect(url_for('auth.login'))
    
@auth.route('/logout')
#logout_user function created and make changes like if u dont have an account but trying to access the logout page it wont work i have rectified it...

def logout():
    session.clear()
    logout_user()
    #route for logging out by above function...
    return redirect(url_for('auth.index'),302)
    
    
@auth.route('/')
def index():
    return render_template('index.html')    



