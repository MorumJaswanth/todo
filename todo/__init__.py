import os
import random
import sys
from flask import Flask, render_template
from flask_login import LoginManager
from flask import g
from . import db

user_id = 0
def create_app(test_config=None):
    app = Flask("todo")
    app.config.from_mapping(
        DATABASE="todo")
    app.config['DATABASE_URL'] = "postgres://fxbqpoixzfjldz:fa03d616c61ded685583bbd92a0c72eebe5afebf24f64695c4aa6380a506b95a@ec2-34-228-100-83.compute-1.amazonaws.com:5432/dbj5h9ssa9ti"
    app.config['SECRET_KEY'] = 'j10a1s19w22a1n14t20h8'
    if test_config is not None:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    

    from . import db 
    db.init_app(app)
        
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from .models import User
    @login_manager.user_loader
    def load_user(userid):
        print(f"{userid}")
        conn=db.get_db()
        cursor=conn.cursor()
        cursor.execute(f"select l.email,l.id from userlist l where id={userid};")
        ret=cursor.fetchall()
        #user=User(userid)
        #return True
        return userid
    # blueprint for auth routes in app
    from . import auth
    app.register_blueprint(auth.auth)
    
    # blueprint for non-auth parts of app  
    from . import todo
    app.register_blueprint(todo.bp)
    
    
        
    return app  
