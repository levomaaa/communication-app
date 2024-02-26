from flask import Flask
from flask import redirect, render_template, request, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import os
from sqlalchemy.sql import text
import secrets

def login(username,password):
    sql = "SELECT id, password FROM users WHERE name=:username"
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
            return True
        else:
            return False

def logout():
    del session["user_id"]
    del session["user_name"]
    del session["csrf_token"]
    return redirect("/")

def user_id():
    return session.get("user_id", 0)

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (name, password) VALUES (:username, :password)"
        db.session.execute(text(sql), {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
