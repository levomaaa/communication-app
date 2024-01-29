from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import os
from sqlalchemy.sql import text

def login(username,password):
    sql = "SELECT id, password FROM users WHERE name=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()    
    if not user:
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["user_id"] = user.id
            session["user_name"] = username
            return True
        else:
            return False

    # TODO: check username and password
    #session["username"] = username
    #return redirect("/")

def logout():
    del session["user_id"]
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