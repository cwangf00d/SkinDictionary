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
    ## Make skincare request based on what you are looking to improve, can select multiple options
    ## Retrieves two products per price category per symptom from database of 101 chemicals and 300 best-selling skincare products
    if request.method == "POST":
        user_requests = []
        low_user_recommendations = []
        mid_user_recommendations = []
        high_user_recommendations = []
        all_recs = []
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
            low_count = 0
            mid_count = 0
            high_count = 0
            to_add_low = db.execute("SELECT prod_loves, prod_price, prod_link, prod_name, prod_brand FROM products WHERE prod_id IN (SELECT prod_id FROM chem_to_prod WHERE chem_id IN (SELECT chem_id FROM symp_to_chem WHERE symp_id IN (SELECT symp_id FROM symptoms WHERE symp_name = ?))) AND prod_price < 15 ORDER BY prod_loves DESC", req)
            to_add_mid = db.execute("SELECT prod_loves, prod_price, prod_link, prod_name, prod_brand FROM products WHERE prod_id IN (SELECT prod_id FROM chem_to_prod WHERE chem_id IN (SELECT chem_id FROM symp_to_chem WHERE symp_id IN (SELECT symp_id FROM symptoms WHERE symp_name = ?))) AND prod_price >14 AND prod_price < 35 ORDER BY prod_loves DESC", req)
            to_add_high = db.execute("SELECT prod_loves, prod_price, prod_link, prod_name, prod_brand FROM products WHERE prod_id IN (SELECT prod_id FROM chem_to_prod WHERE chem_id IN (SELECT chem_id FROM symp_to_chem WHERE symp_id IN (SELECT symp_id FROM symptoms WHERE symp_name = ?))) AND prod_price > 34 ORDER BY prod_loves DESC", req)
            for product in to_add_low:
                if product not in all_recs and low_count < 2:
                    low_user_recommendations.append(product)
                    all_recs.append(product)
                    low_count +=1
            for product in to_add_mid:
                if product not in all_recs and mid_count < 2:
                    mid_user_recommendations.append(product)
                    all_recs.append(product)
                    mid_count +=1
            for product in to_add_high:
                if product not in all_recs and high_count < 2:
                    high_user_recommendations.append(product)
                    all_recs.append(product)
                    high_count +=1
        return render_template("recs.html", lowrec = low_user_recommendations, midrec = mid_user_recommendations, highrec = high_user_recommendations, big_symptom = user_requests, date = date)
    else:
        return render_template("request.html")


@app.route("/compare", methods=["GET", "POST"])
def compare():
    ## allows users to decide, up to 5, skincare products to compare and will provide suggestions of similar products they might want to consider
    if request.method == "POST":
        # Ensure number was submitted
        if not request.form.get("number"):
            return apology("must provide number to compare", 400)
        # Ensure products were submitted
        prod_inventory = db.execute("SELECT prod_id, prod_name FROM products")
        products = []
        for product in prod_inventory:
            if request.form.get('products1') and int(request.form.get('products1')) == product['prod_id']:
                products.append(product['prod_name'])
            elif request.form.get('products2') and int(request.form.get('products2')) == product['prod_id']:
                products.append(product['prod_name'])
            elif request.form.get('products3') and int(request.form.get('products3')) == product['prod_id']:
                products.append(product['prod_name'])
            elif request.form.get('products4') and int(request.form.get('products4')) == product['prod_id']:
                products.append(product['prod_name'])
        all_info = []
        for product in products:
            all_info.append(db.execute("SELECT * FROM products WHERE prod_name = ?", product))
        for big_list in all_info:
            for product in big_list:
                product['prod_chemicals'] = db.execute("SELECT chem_name FROM chemicals WHERE chem_id IN (SELECT chem_id FROM chem_to_prod WHERE prod_id = ?)", product['prod_id'])

        return render_template("comparison.html", size = 4, products = all_info)
    else:
        products = db.execute("SELECT * FROM products")
        return render_template("compare.html", size = 4, products = products)

@app.route("/collection", methods=["GET"])
def collection():
        return render_template("collection.html")

@app.route("/triangle", methods=["GET"])
def triangle():
        return render_template("triangle.html")

@app.route("/vote", methods=["GET", "POST"])
@login_required
def vote():
        return render_template("vote.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
