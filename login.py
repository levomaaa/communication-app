from flask import redirect, request, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from sqlalchemy.sql import text
import secrets

def login(username,password):
    sql = "SELECT id, password, role FROM users WHERE name=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()    
    if not user:
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["user_id"] = user[0]
            session["user_name"] = username
            session["csrf_token"] = secrets.token_hex(16)
            session["user_role"] = user[2]
            return True
        else:
            return False

def logout():
    del session["user_id"]
    del session["user_name"]
    del session["csrf_token"]
    del session["user_role"]
    return redirect("/")

def user_id():
    return session.get("user_id", -1)

def check_role():
    user_role = session["user_role"]
    if user_role != 1:
        abort(403)

def register(username, password):
    hash_value = generate_password_hash(password)
    if user_count() is not None:
        try:
            sql = "INSERT INTO users (name, password) VALUES (:username, :password)"
            db.session.execute(text(sql), {"username":username, "password":hash_value})
            db.session.commit()
        except:
            return False
    else: # First user created will be an admin because the application is only used locally at the moment
        try:
            sql = "INSERT INTO users (name, password, role) " \
                  "VALUES (:username, :password, 1)"
            db.session.execute(text(sql), {"username":username, "password":hash_value})
            db.session.commit()
        except:
            return False        
    return login(username, password)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def user_count():
    sql = "SELECT COUNT(*) FROM users"
    result = db.session.execute(text(sql))
    return result.fetchone()   

def get_users():
    sql = "SELECT id, name FROM users WHERE role IS NULL"
    result = db.session.execute(text(sql))
    return result.fetchall() 

def get_admins():
    sql = "SELECT name FROM users WHERE role=1"
    result = db.session.execute(text(sql))
    return result.fetchall() 

def make_admin(id):
    sql = "UPDATE users SET role=1 WHERE id=:id"
    db.session.execute(text(sql), {"id":id})
    db.session.commit()
    return True