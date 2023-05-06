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
from helpers import apology, login_required

# Global Variables
# These will be used to store your last two programs in case you accidentally leave the app
# The reason this isn't more is that the page would rapidly become way to much.
# This keeps it relatively clean in presentation
HISTORY_1 = []
HISTORY_2 = []

# These will store the total time for the history section
TOTAL_TIME_1 = 0
TOTAL_TIME_2 = 0

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")


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
    # Just renders the index template
    return render_template("index.html")


@app.route("/generate", methods=["GET", "POST"])
@login_required
def generate():
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
            # I make sure they put in a not null value
            try:
                inputted_duration = float(request.form.get("length"))

                # Makes sure they don't change the HTML to go less than 1
                if inputted_duration < 1:
                    return render_template("generate.html")

            # if they did a null value just return them to where they are
            except:
                return render_template("generate.html")

            # Empty list for our program
            program = []

            # to make sure we can have consistent periods no more than 2 apart
            oldPeriod = 0

            # Declares two global variables so we can access them in any function for the time of program
            global TOTAL_TIME_1
            global TOTAL_TIME_2

            # saves the previous total time in the other global variable
            # So we can have the history
            TOTAL_TIME_2 = TOTAL_TIME_1

            # Set time 1 to 0
            TOTAL_TIME_1 = 0
            # This while loop goes through until our program is finished adding each prospective entry
            while inputted_duration >= 0:
                # Genereates a random row from the database
                row = random.randint(0, len(checkov_list))

                # This is the row from the csv that randomly is genereated with all the info for the piece we will use
                # piece is a dict
                piece = checkov_list[row]

                # Gets the period of our piece
                period = int(piece["Period"])

                # We check the difference absolute value of the last period and current
                # We only do it if it is less than or equal to 2.
                # Counter will only happen in the first so we can get any period, but is turned false after the first run
                if abs(period - oldPeriod) <= 2 or counter:
                    # We do try except since some rows do not have a duration value so will give a value error.
                    try:
                        # Gets time of particular piece
                        time = float(piece["Time"])

                        # This makes it so the first piece isn't constrained by any
                        counter = False

                        # Adds it to the total
                        TOTAL_TIME_1 += time

                        # updates new duration
                        inputted_duration -= time

                        # This makes it so the duration never goes too far over inputted
                        if inputted_duration < -2:
                            # Since we didn't use the piece we remove the duration change
                            inputted_duration += time
                            # Just in case we don't use the piece we remove the time from it
                            TOTAL_TIME_1 -= time


                        else:
                            # Updates period so we can keep our distribution
                            oldPeriod = int(piece["Period"])

                            # Adds current piece to list (a list of dicts)
                            program.append(piece)

                    except:
                        print('Row is missing a duration entry and is empty string so we cannot use it!')

            # This rounds to remove floating point inpercision sometiems
            TOTAL_TIME_1 = round(TOTAL_TIME_1, 1)

            # The History global lists are to store the last two programs. We will put whatever was in HISTORY_1
            # into HISTORY_2 and then but program into one. (the first time History 1 is blank)
            # This gives you some insurance in case you close the app

            # We need to refrence them first with global
            global HISTORY_2
            global HISTORY_1

            # Sets are history variables. The first becoems the second here
            HISTORY_2 = HISTORY_1
            HISTORY_1 = program

            # We return all the data including the label of each song since it is built for a radio show
            return render_template("generated.html", program=program, time=TOTAL_TIME_1)

            # The file is auto closed when return from the with statement

    else:
        # This is if you go to page by get
        return render_template("generate.html")


@app.route("/delete", methods=["POST"])
@login_required
def delete():
    # I remove the get method since it shouldn't be used ever. If someone does they will get a 405 error message
    global HISTORY_1
    global TOTAL_TIME_1


    # We go from 0 to one less than length so these aren't allowed
    # We use a try except since if you input null index will have a value error
    try:
        index = int(request.form.get("index"))
        if index < 0 or index >= len(HISTORY_1):
            # We render exactly what we had before since its not in the list
            # This is in case someone changes HTML
            return render_template("generated.html", program=HISTORY_1, time=TOTAL_TIME_1)

        # We remove the inputted index from the History global and we pass into render template
        removed = HISTORY_1.pop(index)

        # this updates total time
        time = float(removed["Time"])
        TOTAL_TIME_1 -= time


        return render_template("generated.html", program=HISTORY_1, time=round(TOTAL_TIME_1, 1))

    except:
        # Keeps the old one if you don't give an index
        return render_template("generated.html", program=HISTORY_1, time=TOTAL_TIME_1)



@app.route("/history")
@login_required
def history():
    # Shows the history of the last two programs

    # Passes in the data to history with the programs and their total times
    return render_template("history.html", HISTORY_1=HISTORY_1, HISTORY_2=HISTORY_2, TOTAL_TIME_1=round(TOTAL_TIME_1, 1), TOTAL_TIME_2=round(TOTAL_TIME_2, 1))



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


