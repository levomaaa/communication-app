from app import app
from flask import render_template, request, redirect, url_for
import login
import forums
import threads
import messages


@app.route("/")
def index():
    count = threads.get_thread_count_of_forum()
    return render_template("index.html", messages=forums.get_forums(), count=count)
    
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
        
        if username == username_check and password1 == password_check and username.isspace() == False and password1.isspace() == False: #pituus viel
            if len(username)>0 or len(password1)>0:
                if password1 != password2:
                    return render_template("error.html", message="Passwords do not match")
                if login.register(username, password1):
                    return redirect("/")
                else:
                    return render_template("error.html", message="Username is already in use")
            else:
                return render_template("error.html", message="Username or password can't be empty")
        else:
            return render_template("error.html", message="Username or password can't contain spaces")

@app.route("/new_forum")
def new():
    return render_template("new_forum.html")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["forumname"]
    " ".join(content.split())
    if len(content)>0 and content.isspace() == False:
        if forums.send(content):
            return redirect("/")
        else:
            return render_template("error.html", message="Failure creating forum")
    else:
        return render_template("error.html", message="Forum name is too short")

@app.route("/edit_forum/<int:forum_id>")
def edit_forum_render(forum_id):
    return render_template("edit_forum.html", forum_id=forum_id, messages=forums.get_forum(forum_id))

@app.route("/editforum/<int:forum_id>", methods=["GET", "POST"])
def editforum(forum_id):
    edited_content = request.form["forumname_edit"]
    " ".join(edited_content.split())
    if len(edited_content)>0 and edited_content.isspace() == False:
        if forums.edit(forum_id,edited_content):
            return redirect("/")
        else:
            return render_template("error.html", message="Failure editing forum")
    else:
        return render_template("error.html", message="Forum name is too short")

@app.route("/delete_forum/<int:forum_id>")
def delete_forum_render(forum_id):
    return render_template("delete_forum.html", forum_id=forum_id, messages=forums.get_forum(forum_id))

@app.route("/deleteforum/<int:forum_id>", methods=["GET", "POST"])
def deleteforum(forum_id):
    if forums.delete(forum_id):
        return redirect("/")
    else:
        return render_template("error.html", message="Failure deleting forum")
    
@app.route("/forum/<int:forum_id>")
def forum(forum_id):
    return render_template("threads.html", threads=threads.get_threads(forum_id), forum=forums.get_forum(forum_id))
    
@app.route("/send_thread/<int:forum_id>", methods=["GET", "POST"])
def send_thread(forum_id):
    content = request.form["threadname"]
    " ".join(content.split())
    if len(content)>0 and content.isspace() == False:
        if threads.send(content,forum_id):
            return redirect(url_for("forum", forum_id=forum_id))
        else:
            return render_template("error.html", message="Failure creating thread")
    else:
        return render_template("error.html", message="Thread name is too short")


@app.route("/new_thread/<int:forum_id>")
def new_thread(forum_id):
    return render_template("new_thread.html", forum=forums.get_forum(forum_id))

@app.route("/edit_thread/<int:thread_id>")
def edit_thread_render(thread_id):
    return render_template("edit_thread.html", thread_id=thread_id, threads=threads.get_thread(thread_id))

@app.route("/editthread/<int:thread_id>", methods=["GET", "POST"])
def editthread(thread_id):
    forum_id = threads.get_forum_id(thread_id)
    forum_id = forum_id[0]
    edited_content = request.form["threadname_edit"]
    " ".join(edited_content.split())
    if len(edited_content)>0 and edited_content.isspace() == False:
        if threads.edit(thread_id,edited_content):
            return redirect(url_for("forum", forum_id=forum_id))
        else:
            return render_template("error.html", message="Failure editing thread")
    else:
        return render_template("error.html", message="Thread name is too short")


@app.route("/delete_thread/<int:thread_id>")
def delete_thread_render(thread_id):
    return render_template("delete_thread.html", thread_id=thread_id, threads=threads.get_thread(thread_id))

@app.route("/deletethread/<int:thread_id>", methods=["GET", "POST"])
def deletethread(thread_id):
    forum_id = threads.get_forum_id(thread_id)
    forum_id = forum_id[0]
    if threads.delete(thread_id):
        return redirect(url_for("forum", forum_id=forum_id))
    else:
        return render_template("error.html", message="Failure deleting thread")
  
@app.route("/thread/<int:thread_id>")
def thread(thread_id):
    return render_template("messages.html", messages=messages.get_messages(thread_id), thread=threads.get_thread(thread_id))
  