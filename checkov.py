import csv
import sys

import os

from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import random
from helpers import apology, login_required, lookup, usd

# declare empty list
# counter = 0
# duration variable = 0
# declare variable oldPeriod = 0
# while duration < inputted duration:
    # i = randomInt(0, len(DictReader))
    # make new variable (piece is a dictionary)-- piece = DictReader[i]
    # find duration of dictionary "piece" -- piece["Time"]
    # find time period of dictionary "piece" -- piece["Period"]
    # if (absolute value of piece["Period"] - oldPeriod <= 2 OR counter == 0)
        # add piece to empty list
        # duration += piece["Duration"]

# to print out final program:
    # return(render_template(index.html), list)

#


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    # Open database csv file:
    if request.method == "POST":
        with open(checkov.csv) as checkov:

            # Read database csv file to dictionary
            checkov_reader = csv.DictReader(checkov)
            counter = True
            # Length they input
            inputted_duration = request.form.get("length")
            # Empty list for our program
            program = []
            duration = 0

            # to make sure we can have consistent periods
            oldPeriod = 0

            while duration <= inputted_duration:
                row = random.randint(0, len(checkov_reader))

                # This is the row from the csv that randomly is genereated with all the info for the piece we will use
                # piece is a dict
                piece = checkov_reader[row]

                period = piece["Period"]

                if abs((period - oldPeriod) <= 2) or counter:
                    # This makes it so the first piece isn't constrained by any
                    counter = False

                    # Adds current piece to list (a list of dicts)
                    program.append(piece)

                    # Checks type of time
                    print(typeof(piece["Time"]))
                    # Casts to flaot
                    time = float(piece["Time"])

                    # updates new duration
                    duration += time

                    # Updates period so we can keep our distribution
                    oldPeriod = piece["Period"]

            return render_template("index.html", piece=piece)

    else:
        return render_template("quote.html")

