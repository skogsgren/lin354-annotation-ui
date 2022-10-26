import os
import xml.etree.ElementTree as ET
import random
import re
from flask_session import Session
from flask import Flask, redirect, render_template, request, session
from functools import wraps
import json
from flaskext.markdown import Markdown

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# For annotation guidelines
Markdown(app)

# Initialize static variables
STATE = "training"  # NOTE: manually set to current annotation stage
if not os.path.exists("annotated_tweets"): os.mkdir("annotated_tweets")
if not os.path.exists(f"annotated_tweets/{STATE}"):
    os.mkdir(f"annotated_tweets/{STATE}")
if not os.path.exists("user_data"): os.mkdir("user_data")
if not os.path.exists(f"user_data/{STATE}"):
    os.mkdir(f"user_data/{STATE}")
# NOTE: Denotes whether or not the website should be user-agnostic (as in
#       the case of pilot annotation) or if each annotator has its own set of
#       tweets to annotate
PER_USER = True if STATE=="training" else False
DATETIME = "20221006121322"  # NOTE: manually set to dataset
with open("dogwhistles.txt", 'r') as f:
    DOGWHISTLES = [x.rstrip() for x in f]
TWT_DIR = f"dataset/{DATETIME}/{STATE}"
TWEETS = [x for x in os.listdir(TWT_DIR)]

# Initialize session variables
session_history, session_tweets = {}, {}

# For displaying annotation guidelines
with open("guidelines.md", 'r') as f:
    md = ''.join(f.readlines())

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def login_required(f):
    """ https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/ """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    uid = session['user_id']  # shorthand
    if request.method == "POST":
        if request.form.get("action") == "undo":
            # get previous item from history stack
            tmp = session["history"].pop()
            # add item back to list of unseen tweets
            session["tweets"].append(tmp)
            # remove xml of previous item
            os.remove(f"annotated_tweets/{STATE}/{uid}/{tmp}")
            # update database on disk
            with open(f"user_data/{STATE}/{uid}.json", 'w') as f:
                json.dump(session, f)
        else:
            # add annotation to xml and write xml to user folder
            action = request.form.get("action")
            filename = request.form.get("filename")
            if PER_USER:
                tree = ET.parse(f"{TWT_DIR}/{uid}/{filename}")
            else:
                tree = ET.parse(f"{TWT_DIR}/{filename}")
            tree.getroot().set("annotation", action)
            tree.write(f"annotated_tweets/{STATE}/{uid}/{filename}")
            # remove tweet xml from choice of next tweet
            twt = session["tweets"].pop(session["tweets"].index(filename))
            # add tweet to history stack
            session["history"].append(twt)
            # update database on disk
            with open(f"user_data/{STATE}/{uid}.json", 'w') as f:
                json.dump(session, f)
        return redirect("/")
    else:
        # If new user: create directories and json file
        if not os.path.exists(f"annotated_tweets/{STATE}/{uid}"):
            os.mkdir(f"annotated_tweets/{STATE}/{uid}")
        if not os.path.exists(f"user_data/{STATE}/{uid}.json"):
            if PER_USER:
                session["tweets"] = [x for x in os.listdir(f"{TWT_DIR}/{uid}")]
            else:
                session["tweets"] = [x for x in TWEETS]
            session["history"] = []
            # write to JSON
            with open(f"user_data/{STATE}/{uid}.json", 'w') as f:
                json.dump(session, f)

        # Load JSON
        with open(f"user_data/{STATE}/{uid}.json", 'r') as f:
            json_data = json.load(f)
            session["tweets"] = json_data["tweets"]
            session["history"] = json_data["history"]


        # If finished annotating, redirect
        if session["tweets"] == []:
            return render_template("finished.html")
        else:
            uid = session["user_id"]
            filename = str(random.choice(session["tweets"]))
            if PER_USER:
                xml = ET.parse(f"{TWT_DIR}/{uid}/{filename}").getroot()
            else:
                xml = ET.parse(f"{TWT_DIR}/{filename}").getroot()
            word = xml.get("word")
            return render_template("index.html",
                                   tweet=xml[0].text,
                                   word=word,
                                   filename=filename,
                                   history=session["history"],
                                   length=len(session["tweets"]),
                                   user_id=uid,
                                   dogwhistles=DOGWHISTLES)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check user-compliance with username guidelines
        username = request.form.get("username")
        if not username:
            return render_template("login.html", failure=True)
        elif " " in username:
            return render_template("login.html", failure=True)
        elif re.search(r"[^a-z]", username):
            return render_template("login.html", failure=True)
        else:
            if PER_USER:
                # conditional to check whether prepared tweets are available
                usrs = [x for x in os.listdir(TWT_DIR) if x[0] not in range(10)]
                if username not in usrs:
                    return redirect("/failure")
            session["user_id"] = username
            return redirect("/")
    return render_template("login.html", failure=False)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/guidelines")
def guidelines():
    return render_template("guidelines.html", md=md)

@app.route("/failure")
def failure():
    return render_template("failure.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
