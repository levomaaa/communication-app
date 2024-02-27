from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import os
from sqlalchemy.sql import text
import login
import forums
import threads

def get_messages(topic_id):
    sql = "SELECT A.id, A.content, U.name, A.sent_at " \
          "FROM adminmessages A, users U " \
          "WHERE A.visible = TRUE " \
          "AND A.topic_id = :topic_id AND U.id = A.user_id " \
          "ORDER BY A.id"
    result = db.session.execute(text(sql), {"topic_id":topic_id})
    return result.fetchall()

def send(content, topic_id):
    user_id = login.user_id()
    user_role = session["user_role"]
    if user_id == 0:
        return False
    if user_role != 1:
        return False
    sql = "INSERT INTO adminmessages (content, user_id, topic_id, sent_at, visible) " \
          "VALUES (:content, :user_id, :topic_id, NOW(), TRUE)"
    db.session.execute(text(sql), {"content":content, "user_id":user_id, "topic_id":topic_id})
    db.session.commit()
    return True