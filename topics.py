from flask import session
from db import db
from sqlalchemy.sql import text
import login

def get_topics():
    sql = "SELECT T.id, T.content, U.name FROM topics T, users U " \
          "WHERE T.user_id = U.id AND T.visible = TRUE ORDER BY T.id"
    result = db.session.execute(text(sql))
    return result.fetchall()

def get_topic(topic_id):
    sql = "SELECT T.id, T.content, U.id FROM topics T, users U " \
          "WHERE T.id = :topic_id AND T.user_id = U.id"
    result = db.session.execute(text(sql), {"topic_id":topic_id})
    return result.fetchall()

def send(content):
    user_id = login.user_id()
    user_role = session["user_role"]
    if user_id == 0:
        return False
    if user_role != 1:
        return False
    sql = "INSERT INTO topics (content, user_id, visible) " \
          "VALUES (:content, :user_id, TRUE)"
    db.session.execute(text(sql), {"content":content, "user_id":user_id})
    db.session.commit()
    return True

def edit(topic_id, edited_content):
    user_role = session["user_role"]
    if user_role != 1:
        return False
    sql = "UPDATE topics SET content = :edited_content " \
          "WHERE id = :topic_id AND :user_role = 1"
    db.session.execute(text(sql), {"topic_id":topic_id, "edited_content":edited_content, "user_role":user_role})
    db.session.commit()
    return True

def delete(topic_id):
    user_role = session["user_role"]
    if user_role != 1:
        return False
    sql = "UPDATE topics SET visible = FALSE WHERE id = :topic_id " \
          "AND :user_role = 1"
    db.session.execute(text(sql), {"topic_id":topic_id, "user_role":user_role})
    db.session.commit()
    return True