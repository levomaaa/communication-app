from app import app
from flask import render_template, request, redirect
import login


@app.route("/")
def index():
    return render_template("index.html")

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
        if password1 != password2:
            return render_template("error.html", message="Passwords do not match")
        if login.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Registeration failed")
            