import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology, usd

import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///skindict.db")

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensure name was submitted
        if not request.form.get("name"):
            return apology("must provide name", 400)

        # Ensure age was submitted
        if not request.form.get("age"):
            return apology("must provide age", 400)

        # Ensure legitimate age was submitted
        if not request.form.get("age").isdigit():
            return apology("must provide real age", 400)

        # Ensure gender was submitted
        if not request.form.get("gender"):
            return apology("must provide gender", 400)

        # Ensure skintype was submitted
        if not request.form.get("skintype"):
            return apology("must provide skintype", 400)

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Ensure username does not already exist
        if len(rows) != 0:
            return apology("username has already been taken", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        if not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)

        # Ensure confirmation and password are the same
        if not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords must match", 400)

        t_username = request.form.get("username")
        t_hash = request.form.get("")
        # Insert user into users
        db.execute("INSERT INTO users (name, username, hash, user_age, user_gender, user_skintype) VALUES (?, ?, ?, ?, ?, ?)", request.form.get("name"), request.form.get("username"), generate_password_hash(request.form.get("password")), request.form.get("age"), request.form.get("gender"), request.form.get("skintype"))
        return redirect("/login")
    else:
        return render_template("register.html")

@app.route("/request", methods=["GET", "POST"])
@login_required
def make_request():
    """Buy shares of stock"""
    if request.method == "POST":
        user_requests = []
        low_user_recommendations = []
        mid_user_recommendations = []
        high_user_recommendations = []
        symptoms = ['uneven skintone', 'acne', 'dullness', 'dryness', 'redness', 'aging', 'sun protectant', 'wound', 'itchiness', 'oiliness', 'exfoliator/cleanser', 'rough', 'discomfort']
        date = datetime.datetime.now()
        # getting which symptoms are being requested
        for symptom in symptoms:
            if request.form.get(symptom):
                user_requests.append(symptom)
                symptom_id = db.execute("SELECT symp_id FROM symptoms WHERE symp_name = ?", symptom)[0]
                db.execute("INSERT INTO user_requests (user_id, symp_id, date) VALUES (?, ?, ?)", session["user_id"], symptom_id['symp_id'], date)
        # iterating through symptoms requested to gather products
        for req in user_requests:
            count = 0
            to_add = db.execute("select a.*, b.chem_id, c.symp_id from products a, chem_to_prod b, symp_to_chem c, symptoms d where d.symp_name=? and d.symp_id=c.symp_id and c.chem_id=b.chem_id and b.prod_id=a.prod_id ORDER BY a.prod_loves DESC", req)
            #to_add = db.execute("SELECT prod_loves, prod_price, prod_link, prod_name, prod_brand FROM products WHERE prod_id IN (SELECT prod_id FROM chem_to_prod WHERE chem_id IN (SELECT chem_id FROM symp_to_chem WHERE symp_id IN (SELECT symp_id FROM symptoms WHERE symp_name = ?))) ORDER BY prod_loves DESC", req)
            for product in to_add:
                if product not in user_recommendations and count < 2:
                    user_recommendations.append(product)
                    count +=1
        return render_template("recs.html", recommendations = user_recommendations, big_symptom = user_requests, date = date)

        # user_requests = []
        # user_recommendations = []
        # symptoms = ['uneven skintone', 'acne', 'dullness', 'dryness', 'redness', 'aging', 'sun protectant', 'wound', 'itchiness', 'oiliness', 'exfoliator/cleanser', 'rough', 'discomfort']
        # date = datetime.datetime.now()
        # # getting which symptoms are being requested
        # for symptom in symptoms:
        #     if request.form.get(symptom):
        #         user_requests.append(symptom)
        #         symptom_id = db.execute("SELECT symp_id FROM symptoms WHERE symp_name = ?", symptom)[0]
        #         db.execute("INSERT INTO user_requests (user_id, symp_id, date) VALUES (?, ?, ?)", session["user_id"], symptom_id['symp_id'], date)
        # # iterating through symptoms requested to gather products
        # for req in user_requests:
        #     count = 0
        #     to_add = db.execute("SELECT prod_loves, prod_price, prod_link, prod_name, prod_brand FROM products WHERE prod_id IN (SELECT prod_id FROM chem_to_prod WHERE chem_id IN (SELECT chem_id FROM symp_to_chem WHERE symp_id IN (SELECT symp_id FROM symptoms WHERE symp_name = ?))) ORDER BY prod_loves DESC", req)
        #     for product in to_add:
        #         if product not in user_recommendations and count < 3:
        #             user_recommendations.append(product)
        #             count +=1
        # return render_template("recs.html", recommendations = user_recommendations, big_symptom = user_requests, date = date)

    else:
        return render_template("request.html")


@app.route("/recs", methods=["GET"])
@login_required
def recs():

    if request.method == "POST":
        return render_template("recs.html")
    else:
        return render_template("request.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
