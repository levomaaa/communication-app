from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import os
from sqlalchemy.sql import text
import login

def get_forums():
    sql = "SELECT F.id, F.content, U.name FROM forums F, users U WHERE F.user_id=U.id"
    result = db.session.execute(text(sql))
    return result.fetchall()

def send(content):
    user_id = login.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO forums (content, user_id) VALUES (:content, :user_id)"
    db.session.execute(text(sql), {"content":content, "user_id":user_id})
    db.session.commit()
    return True