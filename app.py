import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    if not session.get("user_id"):
        return redirect("/login")

    stocks, total, cash = get_user_shares_info()

    stock_shares = {}

    for stock in stocks:
        if not stock["symbol"] in stock_shares:
            stock_shares[stock["symbol"]] = {"symbol": stock["symbol"], "shares": 1, "price": stock["price"], "total": stock["shares"] * stock["price"]}
        else:
            stock_shares[stock["symbol"]]["shares"] += stock["shares"]

    result = []

    for stock_share in stock_shares.values():
        if stock_share["shares"] > 0:
            result.append(stock_share)

    return render_template("index.html", stocks=result, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        stock = lookup(request.form.get("symbol", ""))

        if not request.form.get("symbol"):
            return apology("Symbol cannot be empty")
        if not stock:
            return apology("Stock does not exist")
        if not request.form.get("shares"):
            return apology("Shares cannot be empty")
        if not request.form.get("shares", "1").isdigit():
            return apology("Shares is not a valid number")

        stock_id = db.execute("SELECT id FROM stocks WHERE symbol = ?", request.form["symbol"])

        if not len(stock_id):
            db.execute("INSERT INTO stocks (symbol) VALUES (?)", request.form["symbol"])
            stock_id = db.execute("SELECT id FROM stocks WHERE symbol = ?", request.form["symbol"])

        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        total = int(request.form["shares"]) * stock["price"]

        if cash[0]["cash"] < total:
            return apology("Not enough cash")

        db.execute("INSERT INTO orders (stock_id, user_id, shares) VALUES (?, ?, ?)", stock_id[0]["id"], session["user_id"], request.form["shares"])
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total, session["user_id"])

        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    if not session.get("user_id"):
        return redirect("/login")

    stocks, total, cash = get_user_shares_info()

    return render_template("index.html", stocks=stocks, cash=cash, total=total)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Symbol cannot be empty")

        stock = lookup(request.form["symbol"])

        if not stock:
            return apology("Stock does not exist")

        return render_template("quoted.html", stock=stock)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    def username_exists(username: str | None) -> bool:
        result = db.execute("SELECT id FROM users WHERE username = ?", username)

        return len(result)

    if request.method == "POST":
        username_is_blank = not request.form.get("username")
        passwords_empty = not request.form.get("password") or not request.form.get("confirmation")
        passwords_not_match = request.form.get("password") != request.form.get("confirmation")

        if username_is_blank:
            return apology("Username cannot be empty")
        if username_exists(request.form["username"]):
            return apology("Username already exists")
        if passwords_empty:
            return apology("Password and password confirmation cannot be empty")
        if passwords_not_match:
            return apology("Passwords do not match")

        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            request.form["username"],
            generate_password_hash(request.form["password"])
        )

        return redirect("/login")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    stocks = db.execute("SELECT id, symbol FROM stocks")

    if request.method == "POST":
        stock = [d for d in stocks if d["symbol"] == request.form["symbol"]]

        if not request.form.get("symbol"):
            return apology("Symbol cannot be empty")
        elif not len(stock):
            return apology("Plese select a valid stock")
        elif not request.form.get("shares"):
            return apology("Shares cannot be empty")
        elif (
            not request.form["shares"].isdigit()
            or int(request.form["shares"]) < 1
        ):
            return apology("Shares must have a positive number")

        shares = db.execute("SELECT shares FROM orders WHERE user_id = ? AND stock_id = ?", session["user_id"], stock[0]["id"])

        num_of_shares = 0

        for share in shares:
            num_of_shares += share["shares"]

        if int(request.form["shares"]) > num_of_shares:
            return apology("Not enough shares")

        price = lookup(stock[0]["symbol"])["price"]

        db.execute("INSERT INTO orders (stock_id, user_id, shares) VALUES (?, ?, ?)", stock[0]["id"], session["user_id"], -int(request.form["shares"]))
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", int(request.form["shares"]) * price, session["user_id"])

        return redirect("/")

    return render_template("sell.html", stocks=stocks)

def get_user_shares_info() -> tuple:
    stocks = db.execute("SELECT symbol, shares FROM orders JOIN stocks ON orders.stock_id = stocks.id WHERE user_id = ?", session["user_id"])
    total = 0
    cash = 0

    if len(stocks):
        stocks = add_price(stocks)
        total = sum([s["shares"] * s["price"] for s in stocks])
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    return (stocks, total, cash)

def add_price(stocks: list) -> list:
    for stock in stocks:
        stock["price"] = lookup(stock["symbol"])["price"]

    return stocks