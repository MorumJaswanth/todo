from flask_login import UserMixin
from . import db

class User(UserMixin):
        def __init__(self,id):
            conn=db.get_db()
            cursor=conn.cursor()
            cursor.execute(f"select l.email,l.id from userlist l where id={id};")
            creds=cursor.fetchone()
            self.email=f"{creds[0]}"
            self.userid=f"{creds[1]}"
            self.id=f"{creds[1]}"
        
        def id(self):
            return self.id
        
        def useremail(self):
            return self.email
    
        # def email(self):
            # return self.email
        
        # def is_authenticated(self):
            # return True
        
        # def get_id(self):
            # return self.id
    
        # def is_active(self):
           # return True
        
        # def is_anonymous(self):
            # return False

# class User(UserMixin):
    # def __init__(self, email,id,active=True):
        # self.email=email
        # self.id=id
        
    # def get_id(self):
        # return seld.id
    
    # #def is_active(self):
    # #    return True
    
    # def is_anonymous(self):
        # return False

    # def is_authenticated(self):
        # return True
