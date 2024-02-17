from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import os
from sqlalchemy.sql import text
import login
import forums

def get_threads(forum_id_in):
    sql = "SELECT T.id, T.content, U.name " \
          "FROM threads T, users U " \
          "WHERE T.visible = TRUE " \
          "AND T.forum_id = :forum_id_in AND U.id = T.user_id " \
          "ORDER BY T.id"
    result = db.session.execute(text(sql), {"forum_id_in":forum_id_in})
    return result.fetchall()

def get_thread(thread_id):
    sql = "SELECT id, content FROM threads " \
          "WHERE id = :thread_id"
    result = db.session.execute(text(sql), {"thread_id":thread_id})
    return result.fetchall()

def get_forum_id(thread_id):
    sql = "SELECT forum_id FROM threads " \
          "WHERE id = :thread_id"
    result = db.session.execute(text(sql), {"thread_id":thread_id})
    return result.fetchone()

def get_thread_count():
    sql = "SELECT id, forum_id FROM threads " \
          "WHERE visible = TRUE"
    result = db.session.execute(text(sql))
    return result.fetchall()

def get_thread_count_of_forum():
    list = get_thread_count()
    forum_count = len(forums.get_all_forums())
    count = [0] * (forum_count + 50)
    for i in list:
        t = i[1]
        count[t] += 1
    return count

def send(content, forum_id):
    user_id = login.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO threads (content, user_id, forum_id, visible) " \
          "VALUES (:content, :user_id, :forum_id, TRUE)"
    db.session.execute(text(sql), {"content":content, "user_id":user_id, "forum_id":forum_id})
    db.session.commit()
    return True

def edit(thread_id, edited_content):
    sql = "UPDATE threads SET content = :edited_content " \
          "WHERE id = :thread_id"
    db.session.execute(text(sql), {"thread_id":thread_id, "edited_content":edited_content})
    db.session.commit()
    return True

def delete(thread_id):
    sql = "UPDATE threads SET visible=FALSE WHERE id=:thread_id"
    db.session.execute(text(sql), {"thread_id":thread_id})
    db.session.commit()
    return True