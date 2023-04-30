# Special touch: I made password required to be at least 8 characters, have upper and lower case
# And have a special non alphbetical character.

import os
import csv

from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import random
from helpers import apology, login_required, lookup, usd

# Global Variables
# These will be used to store your last two programs in case you accidentally leave the app
# The reason this isn't more is that the page would rapidly become way to much.
# This keeps it relatively clean in presentation
HISTORY_1 = []
HISTORY_2 = []

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

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    return render_template('index.html')


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    # Open database csv file:
    if request.method == "POST":
        with open("checkov.csv") as checkov:

            # Read database csv file to dictionary
            checkov_reader = csv.DictReader(checkov)

            # Make a list that will become a list of dicts after the for loop
            checkov_list = []
            for row in checkov_reader:
                checkov_list.append(row)

            # This is so the first period will be randomized but the subsequent ones won't be.
            # It will be set to false later so we can get periods that are close
            counter = True

            # Length they input
            inputted_duration = float(request.form.get("length"))

            # Empty list for our program
            program = []

            # to make sure we can have consistent periods
            oldPeriod = 0

            # this keeps track of programs total time
            total_time = 0

            # This while loop goes through until our program is finished adding each prospective entry
            while inputted_duration >= 0:
                row = random.randint(0, len(checkov_list))

                # This is the row from the csv that randomly is genereated with all the info for the piece we will use
                # piece is a dict
                piece = checkov_list[row]

                period = int(piece["Period"])

                if abs((period - oldPeriod) <= 2) or counter:
                    # Casts to flaot, trying to get rid of error
                    try:
                        # This makes it so the first piece isn't constrained by any
                        counter = False

                        time = float(piece["Time"])
                        total_time += time

                        # updates new duration
                        inputted_duration -= time

                        # This makes it so the duration never goes to far over inputted
                        if inputted_duration < -2:
                            # Since we didn't use the piece we remove the duration change
                            inputted_duration += time

                            total_time -= time

                        else:
                            # Updates period so we can keep our distribution
                            oldPeriod = int(piece["Period"])

                            # Adds current piece to list (a list of dicts)
                            program.append(piece)

                    except ValueError:
                        print('Row is missing a duration entry and is empty string so we cannot use it!')

            # This rounds to remove floating point inpercision sometiems
            total_time = round(total_time, 1)

            # The History global lists are to store the last two programs. We will put whatever was in HISTORY_1
            # into HISTORY_2 and then but program into one. (the first time History 1 is blank)
            # This gives you some insurance in case you close the app
            global HISTORY_2
            global HISTORY_1
            HISTORY_2 = HISTORY_1
            HISTORY_1 = program

            print(type(program))
            # We return all the data including the label since this is built for a
            return render_template("quoted.html", program=program, time=total_time)

            # The file is auto closed when return from the with statement

    else:
        return render_template("quote.html")


@app.route("/history")
@login_required
def history():
    # Shows the history of the last two programs

    # Passes in the data to history
    return render_template("history.html", HISTORY_1=HISTORY_1, HISTORY_2=HISTORY_2)



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





@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # having all if shouldn't affect run time since we will be directed out
    # Checks to see if is POST
    if request.method == "POST":
        # Stores username input in variable
        username = request.form.get("username")

        # Checks to see if null
        if not username:
            return apology("Input a username", 400)

        # If this returns non null the username is taken so we return apology
        if db.execute("SELECT username FROM users WHERE username = ?", username):
            return apology("Username already taken", 400)

        password = request.form.get("password")
        # Gets password and checks if null
        if not password:
            return apology("Input a password", 400)

        confirmation = request.form.get("confirmation")

        # Checks if passwords match
        if confirmation != password:
            return apology("Passwords must match", 400)

        # Checks if long enough
        if len(password) < 8:
            return apology("Password must be at least 8 characters!", 400)

        # Checks if has both uppper and lower
        if password.islower() or password.isupper():
            return apology("Password must have an uppercase and lowercase!", 400)

        # Checks for special character in password
        # I could add this above but there will be too many conditions in if
        if password.isalpha():
            return apology("Password must contain at least one non alphabetical character!", 400)

        # I pass in the password variable into the hash function to get a hash of it
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))
        return redirect("/")

    else:
        return render_template("register.html")


