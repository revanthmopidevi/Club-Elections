from flask import Flask, render_template, request, session, redirect, flash
from flask_session import Session
from cs50 import SQL
from flask_bcrypt import Bcrypt
#configure application
app = Flask(__name__)
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = "random string"
Session(app)
# using SQL module from cs50 library
db = SQL("sqlite:///project.db", connect_args={'check_same_thread': False})
# encryption module
bcrypt = Bcrypt(app)
# homepage
@app.route("/")
def index():
    if 'visit' in session:
        return redirect("/logout")
    return render_template('login.html')
# login route
@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'loginID' in session:
            redirect("/")
        input_loginID, input_password = request.form.get('loginID'), request.form.get('password')
        log = db.execute("SELECT * FROM polledID WHERE loginID = :loginID", loginID = input_loginID)
        if len(log) == 1:
            return redirect("/")
        credential = db.execute("SELECT * FROM credentials WHERE loginID = :loginID", loginID = input_loginID)
        if len(credential) == 1 and bcrypt.check_password_hash(credential[0]["password"], input_password):
            db.execute("INSERT INTO polledID (loginID) VALUES(:loginID)", loginID = input_loginID)
            session['visit'] = True
            session['loginID'] = input_loginID
            return render_template("ts.html")
    return redirect("/")
# ballot route
@app.route("/ballot", methods = ['POST'])
def ballot():
    if 'loginID' not in session:
        return redirect("/")
    if request.method == 'POST':
        candidateID = request.form.get('ts')
        candidate = db.execute("SELECT * FROM TS WHERE candidate = :candidateId", candidateId = candidateID)
        current_votes = candidate[0]['votes']
        current_votes += 1
        db.execute("UPDATE TS SET votes = :c_votes WHERE candidate = :candidateId", c_votes = current_votes, candidateId = candidateID)
        return redirect("/logout")
# logout route
@app.route("/logout")
def logout():
    session.pop('loginID', None)
    return render_template("logout.html")

if __name__ == '__main__':
    app.run()
