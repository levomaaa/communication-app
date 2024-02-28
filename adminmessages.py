from flask import redirect, render_template, request, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import os
from sqlalchemy.sql import text
import login
import topics

def get_messages(topic_id):
    login.check_role()
    sql = "SELECT A.id, A.content, U.name, A.sent_at " \
          "FROM adminmessages A, users U " \
          "WHERE A.visible = TRUE " \
          "AND A.topic_id = :topic_id AND U.id = A.user_id " \
          "ORDER BY A.id"
    result = db.session.execute(text(sql), {"topic_id":topic_id})
    return result.fetchall()

def get_message(message_id):
    login.check_role()
    sql = "SELECT A.id, A.content, U.id FROM adminmessages A, users U " \
          "WHERE A.id = :message_id AND A.user_id = U.id"
    result = db.session.execute(text(sql), {"message_id":message_id})
    return result.fetchall()

def send(content, topic_id):
    user_id = login.user_id()
    if user_id == -1:
        return False
    login.check_role()
    sql = "INSERT INTO adminmessages (content, user_id, topic_id, sent_at, visible) " \
          "VALUES (:content, :user_id, :topic_id, NOW(), TRUE)"
    db.session.execute(text(sql), {"content":content, "user_id":user_id, "topic_id":topic_id})
    db.session.commit()
    return True

def edit(message_id, edited_content):
    user_role = session["user_role"]
    login.check_role()
    sql = "UPDATE adminmessages SET content = :edited_content " \
          "WHERE id = :message_id AND :user_role = 1"
    db.session.execute(text(sql), {"message_id":message_id, "edited_content":edited_content, "user_role":user_role})
    db.session.commit()
    return True

def delete(message_id):
    login.check_role()
    user_role = session["user_role"]
    sql = "UPDATE adminmessages SET visible = FALSE WHERE id = :message_id " \
          "AND :user_role = 1"
    db.session.execute(text(sql), {"message_id":message_id, "user_role":user_role})
    db.session.commit()
    return True

def get_topic_id(message_id):
    login.check_role() 
    sql = "SELECT topic_id FROM adminmessages " \
          "WHERE id = :message_id"
    result = db.session.execute(text(sql), {"message_id":message_id})
    return result.fetchone()

def get_message_count():
    login.check_role() 
    sql = "SELECT id, topic_id FROM adminmessages " \
          "WHERE visible = TRUE"
    result = db.session.execute(text(sql))
    return result.fetchall()

def get_message_count_of_topics():
    login.check_role() 
    list = get_message_count()
    topic_count = topics.get_all_topics()
    if topic_count[0] == None:
        count_variable = 0
    else:
        count_variable = topic_count[0]
    count = [0] * (count_variable + 1)
    for i in list:
        t = i[1]
        count[t] += 1
    return count