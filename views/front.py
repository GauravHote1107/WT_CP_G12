from flask import flash, redirect, render_template, request, session, url_for

from database import DatabaseHandler
from reviews import analyze_sentiment, get_comments, get_soup, get_words_count


def check_permissions(func):
    def inner(*args, **kwargs):
        if "name" not in session:
            flash("You cannot access this as you are not logged in!")
            return redirect(url_for("login"))
        else:
            return func(*args, **kwargs)

    return inner


@check_permissions
def about():
    return render_template("aboutUs.html", user=session["name"])


@check_permissions
def contact():
    if request.method == "GET":
        return render_template("contactUs.html", user=session["name"])

    message = request.form.get("message", None)
    if not message:
        flash("Please make sure you enter a message to contact us.")
        return redirect(url_for("dashboard"))

    DatabaseHandler.add_contact(session["id"], session["name"], session["email"], message)

    flash("Thank you for contacting us. Your message is noted and stored successfully!")
    return redirect(url_for("contact"))


@check_permissions
def dashboard():
    if request.method == "GET":
        return render_template("dashboard.html", user=session["name"])

    url = request.form.get("url", None)
    if not url:
        flash("Please make sure you enter a URL to perform the analysis on.")
        return redirect(url_for("dashboard"))

    soup = get_soup(url)
    if not soup:
        flash("Could not fetch the comments for this URL. Make you you've entered a valid URL.")
        return redirect(url_for("dashboard"))

    comments = get_comments(soup)
    sentiments = {}
    reliability = {}

    for comment in comments:
        sentiment = analyze_sentiment(comment["content"])
        sentiments[sentiment] = sentiments.get(sentiment, 0) + 1

        rating = float(comment["rating"].split(" ")[0])

        if rating <= 2 and sentiment != "negative":
            key = "Medium" if sentiment == "neutral" else "Low"
        elif rating == 3 and sentiment != "neutral":
            key = "Medium"
        elif rating >= 4 and sentiment != "positive":
            key = "Medium" if sentiment == "neutral" else "Low"
        else:
            key = "High"

        reliability[key] = reliability.get(key, 0) + 1

    return render_template(
        "analysis.html",
        words=get_words_count(comments),
        sentiments=list(sentiments.items()),
        reliability=list(reliability.items()),
        user=session["name"],
    )
