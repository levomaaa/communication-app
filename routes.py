from app import app
from flask import render_template, request, redirect, url_for, session
import login
import forums
import threads
import messages
from datetime import datetime

@app.route("/")
def index():
    count = threads.get_thread_count_of_forum()
    return render_template("index.html", forums=forums.get_forums(), count=count)
    
@app.route("/login", methods=["GET", "POST"])
def log_in():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if login.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Wrong username or password.")
        
@app.route("/logout")
def logout():
    login.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        username_check = " ".join(username.split())
        password_check = " ".join(password1.split())            
        
        if username == username_check and password1 == password_check and username.isspace() == False and password1.isspace() == False:
            if len(username)>0 and len(password1)>0:
                if len(username)<101 and len(password1)<101:
                    if password1 != password2:
                        return render_template("error.html", message="Passwords do not match")
                    if login.register(username, password1):
                        return redirect("/")
                    else:
                        return render_template("error.html", message="Username is already in use")
                else:
                    return render_template("error.html", message="Username or password is too long")

            else:
                return render_template("error.html", message="Username or password can't be empty")
        else:
            return render_template("error.html", message="Username or password can't contain spaces")

@app.route("/new_forum")
def new():
    return render_template("new_forum.html")

@app.route("/send", methods=["POST"])
def send():
    login.check_csrf()
    content = request.form["forumname"]
    " ".join(content.split())
    if len(content)>0 and content.isspace() == False:
        if len(content)<101:
            if forums.send(content):
                return redirect("/")
            else:
                return render_template("error.html", message="Failure creating forum")
        else:
            return render_template("error.html", message="Forum name is too long")
    else:
        return render_template("error.html", message="Forum name is too short or consists only of spaces")

@app.route("/edit_forum/<int:forum_id>")
def edit_forum_render(forum_id):
    return render_template("edit_forum.html", forum_id=forum_id, forums=forums.get_forum(forum_id))

@app.route("/editforum/<int:forum_id>", methods=["GET", "POST"])
def editforum(forum_id):
    login.check_csrf()
    edited_content = request.form["forumname_edit"]
    " ".join(edited_content.split())
    if len(edited_content)>0 and edited_content.isspace() == False:
        if len(edited_content)<101:
            if forums.edit(forum_id,edited_content):
                return redirect("/")
            else:
                return render_template("error.html", message="Failure editing forum")
        else:
            return render_template("error.html", message="Forum name is too long")
    else:
        return render_template("error.html", message="Forum name is too short or consists only of spaces")

@app.route("/delete_forum/<int:forum_id>")
def delete_forum_render(forum_id):
    return render_template("delete_forum.html", forum_id=forum_id, forums=forums.get_forum(forum_id))

@app.route("/deleteforum/<int:forum_id>", methods=["GET", "POST"])
def deleteforum(forum_id):
    login.check_csrf()
    if forums.delete(forum_id):
        return redirect("/")
    else:
        return render_template("error.html", message="Failure deleting forum")
    
@app.route("/forum/<int:forum_id>")
def forum(forum_id):
    count = messages.get_message_count_of_thread()
    latest_messages = messages.parse_last_message()
    return render_template("threads.html", threads=threads.get_threads(forum_id), forum=forums.get_forum(forum_id), count=count, latest_messages=latest_messages)
    
@app.route("/send_thread/<int:forum_id>", methods=["GET", "POST"])
def send_thread(forum_id):
    login.check_csrf()
    content = request.form["threadname"]
    " ".join(content.split())
    if len(content)>0 and content.isspace() == False:
        if len(content)<101:
            if threads.send(content,forum_id):
                return redirect(url_for("forum", forum_id=forum_id))
            else:
                return render_template("error.html", message="Failure creating thread")
        else:
            return render_template("error.html", message="Thread name is too long")
    else:
        return render_template("error.html", message="Thread name is too short or consists only of spaces")


@app.route("/new_thread/<int:forum_id>")
def new_thread(forum_id):
    return render_template("new_thread.html", forum=forums.get_forum(forum_id))

@app.route("/edit_thread/<int:thread_id>")
def edit_thread_render(thread_id):
    forum_id = threads.get_forum_id(thread_id)
    forum_id = forum_id[0]
    return render_template("edit_thread.html", thread_id=thread_id, threads=threads.get_thread(thread_id), forum=forums.get_forum(forum_id))

@app.route("/editthread/<int:thread_id>", methods=["GET", "POST"])
def editthread(thread_id):
    login.check_csrf()
    forum_id = threads.get_forum_id(thread_id)
    forum_id = forum_id[0]
    edited_content = request.form["threadname_edit"]
    " ".join(edited_content.split())
    if len(edited_content)>0 and edited_content.isspace() == False:
        if len(edited_content)<101:
            if threads.edit(thread_id,edited_content):
                return redirect(url_for("forum", forum_id=forum_id))
            else:
                return render_template("error.html", message="Failure editing thread")
        else:
            return render_template("error.html", message="Thread name is too long")
    else:
        return render_template("error.html", message="Thread name is too short or consists only of spaces")


@app.route("/delete_thread/<int:thread_id>")
def delete_thread_render(thread_id):
    forum_id = threads.get_forum_id(thread_id)
    forum_id = forum_id[0]
    return render_template("delete_thread.html", thread_id=thread_id, threads=threads.get_thread(thread_id), forum=forums.get_forum(forum_id))

@app.route("/deletethread/<int:thread_id>", methods=["GET", "POST"])
def deletethread(thread_id):
    login.check_csrf()
    forum_id = threads.get_forum_id(thread_id)
    forum_id = forum_id[0]
    if threads.delete(thread_id):
        return redirect(url_for("forum", forum_id=forum_id))
    else:
        return render_template("error.html", message="Failure deleting thread")
  
@app.route("/thread/<int:thread_id>")
def thread(thread_id):
    forum_id = threads.get_forum_id(thread_id)
    forum_id = forum_id[0]
    return render_template("messages.html", messages=messages.get_messages(thread_id), thread=threads.get_thread(thread_id), forum=forums.get_forum(forum_id))

@app.route("/new_message/<int:thread_id>")
def new_message(thread_id):
    forum_id = threads.get_forum_id(thread_id)
    forum_id = forum_id[0]
    return render_template("new_message.html", thread=threads.get_thread(thread_id), forum=forums.get_forum(forum_id))

@app.route("/send_message/<int:thread_id>", methods=["GET", "POST"])
def send_message(thread_id):
    login.check_csrf()
    forum_id = threads.get_forum_id(thread_id)
    forum_id = forum_id[0]
    content = request.form["messagename"]
    " ".join(content.split())
    if len(content)>0 and content.isspace() == False:
        if len(content)<5001:
            if messages.send(content,thread_id, forum_id):
                return redirect(url_for("thread", thread_id=thread_id))
            else:
                return render_template("error.html", message="Failure creating thread")
        else:
            return render_template("error.html", message="Message is too long")
    else:
        return render_template("error.html", message="Message is too short or consists only of spaces")

@app.route("/edit_message/<int:message_id>")
def edit_message_render(message_id):
    thread_id = messages.get_thread_id(message_id)
    thread_id = thread_id[0]
    forum_id = threads.get_forum_id(thread_id)
    forum_id = forum_id[0]
    return render_template("edit_message.html", message_id=message_id, message=messages.get_message(message_id), thread=threads.get_thread(thread_id), forum=forums.get_forum(forum_id))

@app.route("/editmessage/<int:message_id>", methods=["GET", "POST"])
def editmessage(message_id):
    login.check_csrf()
    thread_id = messages.get_thread_id(message_id)
    thread_id = thread_id[0]
    edited_content = request.form["messagename_edit"]
    " ".join(edited_content.split())
    if len(edited_content)>0 and edited_content.isspace() == False:
        if len(edited_content)<5001:
            if messages.edit(message_id,edited_content):
                return redirect(url_for("thread", thread_id=thread_id))
            else:
                return render_template("error.html", message="Failure editing message")
        else:
            return render_template("error.html", message="Message is too long")
    else:
        return render_template("error.html", message="Message is too short or consists only of spaces")

@app.route("/delete_message/<int:message_id>")
def delete_message_render(message_id):
    thread_id = messages.get_thread_id(message_id)
    thread_id = thread_id[0]
    forum_id = threads.get_forum_id(thread_id)
    forum_id = forum_id[0]
    return render_template("delete_message.html", message_id=message_id, message=messages.get_message(message_id), thread=threads.get_thread(thread_id), forum=forums.get_forum(forum_id))

@app.route("/deletemessage/<int:message_id>", methods=["GET", "POST"])
def deletemessage(message_id):
    login.check_csrf()
    thread_id = messages.get_thread_id(message_id)
    thread_id = thread_id[0]
    if messages.delete(message_id):
        return redirect(url_for("thread", thread_id=thread_id))
    else:
        return render_template("error.html", message="Failure deleting message")
 
@app.route("/adminpage")
def adminpage():
    #count = adminthreads.get_message_count()
    return render_template("adminpage.html")#, threads=adminthreads.get_threads(), count=count)
   