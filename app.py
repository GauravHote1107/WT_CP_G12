import redis
from flask import Flask, get_flashed_messages
from flask_session import Session

import views.auth
import views.front

app = Flask(__name__)

app.config["SECRET_KEY"] = "4d56106a0b060a51eb08e2b0431d45e0b142c963c86aec47"
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_REDIS"] = redis.from_url("redis://127.0.0.1:6379")

Session(app)

app.add_url_rule("/", "login", views.auth.login, methods=["GET", "POST"])

app.add_url_rule("/register", "register", views.auth.register, methods=["GET", "POST"])
app.add_url_rule("/logout", "logout", views.auth.logout)

app.add_url_rule("/dashboard", "dashboard", views.front.dashboard, methods=["GET", "POST"])
app.add_url_rule("/contact", "contact", views.front.contact, methods=["GET", "POST"])
app.add_url_rule("/about", "about", views.front.about)

if __name__ == "__main__":
    app.run(debug=True)
