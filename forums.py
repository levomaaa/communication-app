from flask import session
from sqlalchemy.sql import text
from db import db
import login

def get_forums():
    sql = "SELECT F.id, F.content, U.name FROM forums F, users U " \
          "WHERE F.user_id=U.id AND F.visible=TRUE ORDER BY F.id"
    result = db.session.execute(text(sql))
    return result.fetchall()

def get_forum(forum_id):
    sql = "SELECT F.id, F.content, U.id FROM forums F, users U " \
          "WHERE F.id=:forum_id AND F.user_id=U.id"
    result = db.session.execute(text(sql), {"forum_id":forum_id})
    return result.fetchall()

def get_all_forums():
    sql = "SELECT MAX(id) FROM forums"
    result = db.session.execute(text(sql))
    return result.fetchone()   

def send(content):
    user_id = login.user_id()
    if user_id == -1:
        return False
    sql = "INSERT INTO forums (content, user_id, visible) VALUES (:content, :user_id, TRUE)"
    db.session.execute(text(sql), {"content":content, "user_id":user_id})
    db.session.commit()
    return True

def edit(forum_id, edited_content):
    user_id = session["user_id"]
    user_role = session["user_role"]
    sql = "UPDATE forums SET content=:edited_content " \
          "WHERE id=:forum_id AND (user_id=:user_id OR :user_role=1)"
    db.session.execute(text(sql), {"forum_id":forum_id, "edited_content":edited_content, "user_id":user_id, "user_role":user_role})
    db.session.commit()
    return True

def delete(forum_id):
    user_id = session["user_id"]
    user_role = session["user_role"]
    sql = "UPDATE forums SET visible=FALSE WHERE id=:forum_id " \
          "AND (user_id=:user_id OR :user_role=1)"
    db.session.execute(text(sql), {"forum_id":forum_id, "user_id":user_id, "user_role":user_role})
    db.session.commit()
    return True

def if_exists(name):
    sql = "SELECT content FROM forums WHERE content=:name " \
          "AND visible=TRUE"
    result = db.session.execute(text(sql), {"name":name})
    result = result.fetchone()
    if_exists = result
    variable = [""]
    if if_exists is None:
        variable[0] = ""
    else:
        variable[0] = if_exists[0]
    return variable[0]