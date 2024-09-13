from flask import flash, redirect, render_template, request, session, url_for
from passlib.hash import pbkdf2_sha256

from database import DatabaseHandler


def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", None)
    password = request.form.get("password", None)

    if not email or not password:
        flash("Invalid login details entered, please fill out all fields.")
        return render_template("login.html")

    user = DatabaseHandler.get_user(email)
    if not user or not pbkdf2_sha256.verify(password, user[3]):
        flash("Incorrect credentials entered, please check your details.")
        return render_template("login.html")

    session["id"] = user[0]
    session["name"] = user[1]
    session["email"] = user[2]

    return redirect(url_for("dashboard"))


def register():
    if request.method == "GET":
        return redirect("/login")

    name = request.form.get("name", None)
    email = request.form.get("email", None)
    password = request.form.get("password", None)

    if not name or not email or not password:
        flash("Invalid registration details entered.")
        return redirect(url_for("login"))

    if id := DatabaseHandler.register_user(name, email, pbkdf2_sha256.hash(password)):
        session["id"] = id
        session["name"] = name
        session["email"] = email
        return redirect(url_for("dashboard"))
    else:
        flash("The email address you're trying to register with is taken.")

    return redirect(url_for("login"))


def logout():
    session.clear()
    return redirect(url_for("login"))
