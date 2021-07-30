import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify, session,flash
from flask import g
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
from .models import User
from . import db

bp = Blueprint("todo", "todo", url_prefix="")

@bp.route("/page")
def dashboard():
    oby=["taskname","taskdescription","deadline","deadline_time","status"]
    uid=session.get("user_id")
    conn=db.get_db()
    cursor=conn.cursor()
    cursor.execute(f"select DISTINCT u.id, u.taskname, u.taskdescription, u.deadline, u.deadline_time, u.status from user_ u, userlist l where u.userid=l.id and l.id={uid} order by u.deadline, u.deadline_time;")
    tasks=cursor.fetchall()
    cursor.execute(f"select l.name from userlist l WHERE l.id={uid};")
    name=cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT (u.id) FROM user_ u,userlist l WHERE u.deadline = CURRENT_DATE AND u.userid=l.id AND l.id={uid};")
    today=cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT (u.id) FROM user_ u,userlist l WHERE u.deadline BETWEEN CURRENT_DATE AND CURRENT_DATE + INTEGER'7' AND u.userid=l.id AND l.id={uid};")
    thisweek=cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT (u.id) FROM user_ u,userlist l WHERE u.deadline < CURRENT_DATE AND u.userid=l.id AND l.id={uid};")
    overdue=cursor.fetchone()[0]
    return render_template('todo.html',tasks=tasks,name=name,today=today,thisweek=thisweek,overdue=overdue)
    

   
@bp.route("/addnewtopic",methods=["GET","POST"])
def addnewtopic():
    if request.method=="GET":
        return render_template('edit.html')
    elif request.method=="POST":
        taskname=request.form.get('taskname')
        taskdescription=request.form.get('taskdescription')
        deadline=request.form.get('deadline')
        deadline_time=request.form.get('deadline_time')
        uid=session.get("user_id")
        conn=db.get_db()
        cursor=conn.cursor()
        cursor.execute(f"INSERT into user_(taskname,taskdescription,deadline,deadline_time,status,userid) values ('{taskname}','{taskdescription}','{deadline}','{deadline_time}','pending',{uid})")
        conn.commit()
        return redirect(url_for("todo.dashboard"),302)
 
 
@bp.route("/<tid>/edit",methods=['GET','POST'])
def edit(tid):
    conn=db.get_db()
    cursor=conn.cursor()
    if request.method=="GET":
        cursor.execute(f"select u.taskname, u.taskdescription, u.deadline, u.deadline_time from user_ u where u.id={tid}")
        details=cursor.fetchone()
        taskname, taskdescription, deadline, deadline_time= details
        return render_template('edittask.html', taskname=taskname, taskdescription=taskdescription, deadline=deadline, deadline_time=deadline_time,tid=tid)
    elif request.method=="POST":
        taskname=request.form.get('taskname')
        taskdescription=request.form.get('taskdescription')
        deadline=request.form.get('deadline')
        deadline_time=request.form.get('deadline_time')
        status=request.form.get('status')
        if status=='done':
            cursor.execute("update user_ set taskname = %s, taskdescription=%s, deadline=%s, deadline_time=%s, status='Done' where id=%s", (taskname, taskdescription,deadline,deadline_time,tid))
        else:
            cursor.execute("update user_ set taskname = %s, taskdescription=%s, deadline=%s, deadline_time=%s where id=%s", (taskname, taskdescription,deadline,deadline_time,tid))
        conn.commit()
        return redirect(url_for("todo.dashboard"),302)
        

@bp.route("/<tid>/delete")
def delete(tid):
    conn=db.get_db()
    cursor=conn.cursor()
    cursor.execute(f"DELETE FROM user_ WHERE id={tid};")
    conn.commit()
    flash('Successfully Deleted..','success')
    return redirect(url_for("todo.dashboard"),302)

@bp.route("/sort",methods=['GET','POST'])
def sort():
    if request.method=="POST":
        sd=request.form.get('sd')
        ed=request.form.get('ed')
        st=request.form.get('st')
        et=request.form.get('et')
        uid=session.get("user_id")
        conn=db.get_db()
        cursor=conn.cursor()
        cursor.execute(f"select u.id, u.taskname, u.taskdescription, u.deadline, u.deadline_time, u.status from user_ u WHERE deadline_time BETWEEN %s AND %s AND u.id IN (select u.id from user_ u, userlist l where u.deadline BETWEEN %s AND %s AND u.userid=l.id AND l.id={uid});",(st,et,sd,ed))
        tasks=cursor.fetchall()
        otpt=(f"{uid} sd = {st} \n ed={et} \n {tasks}")
        cursor.execute(f"select l.name from userlist l;")
        name=cursor.fetchone()[0]
        return render_template('todo.html',tasks=tasks,name=name)

        
