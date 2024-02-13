from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import os
from sqlalchemy.sql import text
import login


def get_threads(forum_id_in):
    sql = "SELECT T.id, T.content, U.name " \
          "FROM threads T, users U " \
          "WHERE T.visible = TRUE " \
          "AND T.forum_id = :forum_id_in AND U.id = T.user_id"
    result = db.session.execute(text(sql), {"forum_id_in":forum_id_in})
    return result.fetchall()

def send(content, forum_id):
    user_id = login.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO threads (content, user_id, forum_id, visible) " \
          "VALUES (:content, :user_id, :forum_id, TRUE)"
    db.session.execute(text(sql), {"content":content, "user_id":user_id, "forum_id":forum_id})
    db.session.commit()
    return True