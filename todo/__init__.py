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
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    #app.config['uid']=150
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
        user=User(userid)
        #return True
        return User(userid)
    # blueprint for auth routes in app
    from . import auth
    app.register_blueprint(auth.auth)
    
    # blueprint for non-auth parts of app  
    from . import todo
    app.register_blueprint(todo.bp)
    
    
        
    return app  
