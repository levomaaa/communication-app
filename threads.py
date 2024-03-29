from flask import session
from db import db
from sqlalchemy.sql import text
import login
import forums

def get_threads(forum_id_in):
    sql = "SELECT T.id, T.content, U.name " \
          "FROM threads T, users U " \
          "WHERE T.visible=TRUE " \
          "AND T.forum_id=:forum_id_in AND U.id=T.user_id " \
          "ORDER BY T.id"
    result = db.session.execute(text(sql), {"forum_id_in":forum_id_in})
    return result.fetchall()

def get_thread(thread_id):
    sql = "SELECT T.id, T.content, U.id FROM threads T, users U " \
          "WHERE T.id=:thread_id AND T.user_id=U.id"
    result = db.session.execute(text(sql), {"thread_id":thread_id})
    return result.fetchall()

def get_all_threads():
    sql = "SELECT MAX(id) FROM threads"
    result = db.session.execute(text(sql))
    return result.fetchone()   

def get_forum_id(thread_id):
    sql = "SELECT forum_id FROM threads " \
          "WHERE id=:thread_id"
    result = db.session.execute(text(sql), {"thread_id":thread_id})
    return result.fetchone()

def get_thread_count():
    sql = "SELECT id, forum_id FROM threads " \
          "WHERE visible=TRUE"
    result = db.session.execute(text(sql))
    return result.fetchall()

def get_thread_count_of_forum():
    list = get_thread_count()
    forum_count = forums.get_all_forums()
    if forum_count[0] is None:
        count_variable = 0
    else:
        count_variable = forum_count[0]
    count = [0] * (count_variable + 1)
    for i in list:
        t = i[1]
        count[t] += 1
    return count

def send(content, forum_id):
    user_id = login.user_id()
    if user_id == -1:
        return False
    sql = "INSERT INTO threads (content, user_id, forum_id, visible) " \
          "VALUES (:content, :user_id, :forum_id, TRUE)"
    db.session.execute(text(sql), {"content":content, "user_id":user_id, "forum_id":forum_id})
    db.session.commit()
    return True

def edit(thread_id, edited_content):
    user_id = session["user_id"]
    user_role = session["user_role"]
    sql = "UPDATE threads SET content=:edited_content " \
          "WHERE id=:thread_id AND (user_id=:user_id OR :user_role=1)"
    db.session.execute(text(sql), {"thread_id":thread_id, \
                                    "edited_content":edited_content, "user_id":user_id, \
                                          "user_role":user_role})
    db.session.commit()
    return True

def delete(thread_id):
    user_id = session["user_id"]
    user_role = session["user_role"]
    sql = "UPDATE threads SET visible=FALSE WHERE id=:thread_id " \
          "AND (user_id=:user_id OR :user_role=1)"
    db.session.execute(text(sql), {"thread_id":thread_id, "user_id":user_id, "user_role":user_role})
    db.session.commit()
    return True

def if_exists(name, forum_id):
    sql = "SELECT content FROM threads WHERE content=:name " \
          "AND visible=TRUE AND forum_id=:forum_id"
    result = db.session.execute(text(sql), {"name":name, "forum_id":forum_id})
    result = result.fetchone()
    if_exists = result
    variable = [""]
    if if_exists is None:
        variable[0] = ""
    else:
        variable[0] = if_exists[0]
    return variable[0]