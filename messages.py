from flask import session
from db import db
from sqlalchemy.sql import text
import login
import threads

def get_messages(thread_id):
    sql = "SELECT M.id, M.content, U.name, M.sent_at " \
          "FROM messages M, users U " \
          "WHERE M.visible=TRUE " \
          "AND M.thread_id=:thread_id AND U.id=M.user_id " \
          "ORDER BY M.id"
    result = db.session.execute(text(sql), {"thread_id":thread_id})
    return result.fetchall()

def get_message(message_id):
    sql = "SELECT M.id, M.content, U.id FROM messages M, users U " \
          "WHERE M.id=:message_id AND M.user_id=U.id"
    result = db.session.execute(text(sql), {"message_id":message_id})
    return result.fetchall()

def send(content, thread_id, forum_id):
    user_id = login.user_id()
    if user_id == -1:
        return False
    sql = "INSERT INTO messages (content, user_id, thread_id, " \
          "forum_id, sent_at, visible) VALUES (:content, :user_id, " \
          ":thread_id, :forum_id, NOW(), TRUE)"
    db.session.execute(text(sql), {"content":content, "user_id":user_id, \
                                    "thread_id":thread_id, "forum_id":forum_id})
    db.session.commit()
    return True

def get_message_count():
    sql = "SELECT id, thread_id FROM messages " \
          "WHERE visible=TRUE"
    result = db.session.execute(text(sql))
    return result.fetchall()

def get_message_count_of_thread():
    list = get_message_count()
    thread_count = threads.get_all_threads()
    if thread_count[0] is None:
        count_variable = 0
    else:
        count_variable = thread_count[0]
    count = [0] * (count_variable + 1)
    for i in list:
        t = i[1]
        count[t] += 1
    return count

def get_last_message(thread_id):
    sql = "SELECT sent_at FROM messages " \
          "WHERE visible=TRUE AND thread_id=:thread_id " \
          "ORDER BY sent_at DESC LIMIT 1"
    result = db.session.execute(text(sql), {"thread_id":thread_id})
    return result.fetchone()

def parse_last_message():
    list = threads.get_thread_count()
    thread_count = threads.get_all_threads()
    if thread_count[0] is None:
        count_variable = 0
    else: 
        count_variable = thread_count[0]
    latest_messages = [0] * (count_variable + 1)
    for i in list:
        t = i[0]
        time = get_last_message(t)
        if time is not None:
            time = time.__str__()
            time = time.replace('datetime', '')
            time = time.replace('(', '')
            time = time.replace(')', '')
            time = time.replace('.', '')
            time = time[:-1]
            times = time.split()
            for j in range(len(times)):
                if len(times[j])<3:
                    times[j] = "0" + times[j]
            time = times[0] + "-" + times[1] + "-" + times[2] \
                  + " " + times[3] + ":" + times[4] + ":" + times[5]
            time = time.replace(',', '')
            latest_messages[t] = time
        else:
            latest_messages[t] = 'No messages yet'
    return latest_messages

def get_thread_id(message_id):
    sql = "SELECT thread_id FROM messages " \
          "WHERE id=:message_id"
    result = db.session.execute(text(sql), {"message_id":message_id})
    return result.fetchone()

def edit(message_id, edited_content):
    user_id = session["user_id"]
    user_role = session["user_role"]
    sql = "UPDATE messages SET content=:edited_content " \
          "WHERE id=:message_id AND (user_id=:user_id OR :user_role=1)"
    db.session.execute(text(sql), {"message_id":message_id, "edited_content":edited_content, \
                                   "user_id":user_id, "user_role":user_role})
    db.session.commit()
    return True

def delete(message_id):
    user_id = session["user_id"]
    user_role = session["user_role"]
    sql = "UPDATE messages SET visible=FALSE WHERE id=:message_id " \
          "AND (user_id=:user_id OR :user_role=1)"
    db.session.execute(text(sql), {"message_id":message_id, \
                                    "user_id":user_id, "user_role":user_role})
    db.session.commit()
    return True