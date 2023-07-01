import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

MONTHS = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}
DAYS = tuple(range(1, 32))

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    birthdays = db.execute("SELECT * FROM birthdays")
    error = ""

    if request.method == "POST":
        if(not request.form.get("name")
           or int(request.form.get("month")) not in MONTHS
           or int(request.form.get("day")) not in DAYS):
            error = "Invalid input, make sure you have entered all data and that it is valid"
        else:
            db.execute(
                "INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)",
                request.form["name"],
                request.form["month"],
                request.form["day"]
            )

    return render_template("index.html", months=MONTHS, days=DAYS, error=error, birthdays=birthdays)


