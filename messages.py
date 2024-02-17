from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import os
from sqlalchemy.sql import text
import login
import forums
import threads

def get_messages(thread_id):
    sql = "SELECT M.id, M.content, U.name, M.sent_at " \
          "FROM messages M, users U " \
          "WHERE M.visible = TRUE " \
          "AND M.thread_id = :thread_id AND U.id = M.user_id " \
          "ORDER BY M.id"
    result = db.session.execute(text(sql), {"thread_id":thread_id})
    return result.fetchall()

def send(content, thread_id, forum_id):
    user_id = login.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO messages (content, user_id, thread_id, forum_id, sent_at, visible) " \
          "VALUES (:content, :user_id, :thread_id, :forum_id, NOW(), TRUE)"
    db.session.execute(text(sql), {"content":content, "user_id":user_id, "thread_id":thread_id, "forum_id":forum_id})
    db.session.commit()
    return True