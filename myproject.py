from flask import Flask, render_template, session,request, redirect, flash
from flask_session import Session
from cs50 import SQL
from flask_bcrypt import Bcrypt

#configure application
app = Flask(__name__)
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = "secret_key"
Session(app)
# using SQL module from cs50 library
db = SQL("sqlite:///project.db", connect_args={'check_same_thread': False})
# encryption module
bcrypt = Bcrypt(app)

# LANDING PAGE
@app.route("/")
def index():
    return render_template('login.html')

# LOGIN ROUTE
@app.route("/login", methods = ['POST'])
def login():
    if request.method == 'POST':
        if 'loginID' in session:
            return redirect("/logout")

        loginID = request.form.get('loginID')
        password = request.form.get('password')
        club = request.form.get('club')

        loginID = loginID.lower()
        clubID = club + 'ID'
        clubpolledID = club + "polledID"

        # validate input
        if len(loginID) != 9 or not loginID.isalnum():
            return redirect("/")
        elif len(password) != 15 or not password.isalnum():
            return redirect("/")
        
        # check if already logged in
        polled = db.execute("SELECT * FROM :club_polled_ID WHERE loginID = :login_ID", club_polled_ID = clubpolledID, login_ID = loginID)
        if len(polled) == 1:
            return redirect("/logout")
        
        # validate credentials
        member = db.execute("SELECT * FROM :club_ID WHERE loginID = :login_ID", club_ID = clubID, login_ID = loginID)
        if len(member) == 1:
            if bcrypt.check_password_hash(member[0]['password'], password):
                db.execute("INSERT INTO :club_polled_ID VALUES(:login_ID)", club_polled_ID = clubpolledID, login_ID = loginID)
                session['loginID'] = loginID
                session['club'] = club
                return render_template(f"{club}.html")
    return redirect("/")    


# ballot route for COOKING
@app.route("/COOKING", methods = ['POST'])
def Cooking():
    if 'loginID' not in session or 'club' not in session:
        return redirect("/")

    if session['club'] != 'COOKING':
        return redirect("/")

    if request.method == 'POST':
        # update votes for Joint Secretary
        JScandidateID = request.form.get('JS')
        if JScandidateID.isalpha():
            JScandidate = db.execute("SELECT * FROM COOKINGvotes WHERE candidateID = :JScandidate_ID", JScandidate_ID = JScandidateID)
        else:
            return redirect("/")
        JScurrent_votes = JScandidate[0]['votes']
        JScurrent_votes += 1
        db.execute("UPDATE COOKINGvotes SET votes = :JSc_votes WHERE candidateID = :JScandidate_ID", JSc_votes = JScurrent_votes, JScandidate_ID = JScandidateID)
        # update votes for Treasurer
        TcandidateID = request.form.get('T')
        if TcandidateID.isalpha():
            Tcandidate = db.execute("SELECT * FROM COOKINGvotes WHERE candidateID = :Tcandidate_ID", Tcandidate_ID = TcandidateID)
        else:
            return redirect("/")
        Tcurrent_votes = Tcandidate[0]['votes']
        Tcurrent_votes += 1
        db.execute("UPDATE COOKINGvotes SET votes = :Tc_votes WHERE candidateID = :Tcandidate_ID", Tc_votes = Tcurrent_votes, Tcandidate_ID = TcandidateID)
        # logout
        return redirect("/logout")


# ballot route for DANCE
@app.route("/DANCE", methods = ['POST'])
def Dance():
    if 'loginID' not in session or 'club' not in session:
        return redirect("/")

    if session['club'] != 'DANCE':
        return redirect("/")

    if request.method == 'POST':
        # update votes for Secretary
        ScandidateID = request.form.get('S')
        if ScandidateID.isalpha():
            Scandidate = db.execute("SELECT * FROM DANCEvotes WHERE candidateID = :Scandidate_ID", Scandidate_ID = ScandidateID)
        else:
            return redirect("/")
        Scurrent_votes = Scandidate[0]['votes']
        Scurrent_votes += 1
        db.execute("UPDATE DANCEvotes SET votes = :Sc_votes WHERE candidateID = :Scandidate_ID", Sc_votes = Scurrent_votes, Scandidate_ID = ScandidateID)
        # update votes for Coordinator
        CcandidateID = request.form.get('C')
        if CcandidateID.isalpha():
            Ccandidate = db.execute("SELECT * FROM DANCEvotes WHERE candidateID = :Ccandidate_ID", Ccandidate_ID = CcandidateID)
        else:
            return redirect("/")
        Ccurrent_votes = Ccandidate[0]['votes']
        Ccurrent_votes += 1
        db.execute("UPDATE DANCEvotes SET votes = :Cc_votes WHERE candidateID = :Ccandidate_ID", Cc_votes = Ccurrent_votes, Ccandidate_ID = CcandidateID)
        # logout
        return redirect("/logout")

# ballot route for DRAMA
@app.route("/DRAMA", methods = ['POST'])
def Drama():
    if 'loginID' not in session or 'club' not in session:
        return redirect("/")

    if session['club'] != 'DRAMA':
        return redirect("/")

    if request.method == 'POST':
        # update votes for Secretary
        ScandidateID = request.form.get('S')
        if ScandidateID.isalpha():
            Scandidate = db.execute("SELECT * FROM DRAMAvotes WHERE candidateID = :Scandidate_ID", Scandidate_ID = ScandidateID)
        else:
            return redirect("/")
        Scurrent_votes = Scandidate[0]['votes']
        Scurrent_votes += 1
        db.execute("UPDATE DRAMAvotes SET votes = :Sc_votes WHERE candidateID = :Scandidate_ID", Sc_votes = Scurrent_votes, Scandidate_ID = ScandidateID)
        # logout
        return redirect("/logout")

# ballot route for ELAS
@app.route("/ELAS", methods = ['POST'])
def ELAS():
    if 'loginID' not in session or 'club' not in session:
        return redirect("/")

    if session['club'] != 'ELAS':
        return redirect("/")

    if request.method == 'POST':
        # update votes for Joint Secretary
        JScandidateID = request.form.get('JS')
        if JScandidateID.isalpha():
            JScandidate = db.execute("SELECT * FROM ELASvotes WHERE candidateID = :JScandidate_ID", JScandidate_ID = JScandidateID)
        else:
            return redirect("/")
        JScurrent_votes = JScandidate[0]['votes']
        JScurrent_votes += 1
        db.execute("UPDATE ELASvotes SET votes = :JSc_votes WHERE candidateID = :JScandidate_ID", JSc_votes = JScurrent_votes, JScandidate_ID = JScandidateID)
        # update votes for Treasurer
        TcandidateID = request.form.get('T')
        if TcandidateID.isalpha():
            Tcandidate = db.execute("SELECT * FROM ELASvotes WHERE candidateID = :Tcandidate_ID", Tcandidate_ID = TcandidateID)
        else:
            return redirect("/")
        Tcurrent_votes = Tcandidate[0]['votes']
        Tcurrent_votes += 1
        db.execute("UPDATE ELASvotes SET votes = :Tc_votes WHERE candidateID = :Tcandidate_ID", Tc_votes = Tcurrent_votes, Tcandidate_ID = TcandidateID)
        # logout
        return redirect("/logout")

# ballot route for JC
@app.route("/JC", methods = ['POST'])
def JC():
    if 'loginID' not in session or 'club' not in session:
        return redirect("/")

    if session['club'] != 'JC':
        return redirect("/")

    if request.method == 'POST':
        # update votes for Treasurer
        TcandidateID = request.form.get('T')
        if TcandidateID.isalpha():  
            Tcandidate = db.execute("SELECT * FROM JCvotes WHERE candidateID = :Tcandidate_ID", Tcandidate_ID = TcandidateID)
        else:
            return redirect("/")
        Tcurrent_votes = Tcandidate[0]['votes']
        Tcurrent_votes += 1
        db.execute("UPDATE JCvotes SET votes = :Tc_votes WHERE candidateID = :Tcandidate_ID", Tc_votes = Tcurrent_votes, Tcandidate_ID = TcandidateID)
        # logout
        return redirect("/logout")

# ballot route for PHOTOG
@app.route("/PHOTOG", methods = ['POST'])
def Photog():
    if 'loginID' not in session or 'club' not in session:
        return redirect("/")

    if session['club'] != 'PHOTOG':
        return redirect("/")

    if request.method == 'POST':
        # update votes for Secretary
        ScandidateID = request.form.get('S')
        if ScandidateID.isalpha():
            Scandidate = db.execute("SELECT * FROM PHOTOGvotes WHERE candidateID = :Scandidate_ID", Scandidate_ID = ScandidateID)
        else:
            return redirect("/")
        Scurrent_votes = Scandidate[0]['votes']
        Scurrent_votes += 1
        db.execute("UPDATE PHOTOGvotes SET votes = :Sc_votes WHERE candidateID = :Scandidate_ID", Sc_votes = Scurrent_votes, Scandidate_ID = ScandidateID)
        # logout
        return redirect("/logout")

# ballot route for SAFL
@app.route("/SAFL", methods = ['POST'])
def SAFL():
    if 'loginID' not in session or 'club' not in session:
        return redirect("/")

    if session['club'] != 'SAFL':
        return redirect("/")

    if request.method == 'POST':
        # update votes for Joint Secretary
        JScandidateID = request.form.get('JS')
        if JScandidateID.isalpha(): 
            JScandidate = db.execute("SELECT * FROM SAFLvotes WHERE candidateID = :JScandidate_ID", JScandidate_ID = JScandidateID)
        else:
            return redirect("/")
        JScurrent_votes = JScandidate[0]['votes']
        JScurrent_votes += 1
        db.execute("UPDATE SAFLvotes SET votes = :JSc_votes WHERE candidateID = :JScandidate_ID", JSc_votes = JScurrent_votes, JScandidate_ID = JScandidateID)
        # logout
        return redirect("/logout")

# ballot route for SHADES
@app.route("/SHADES", methods = ['POST'])
def Shades():
    if 'loginID' not in session or 'club' not in session:
        return redirect("/")

    if session['club'] != 'SHADES':
        return redirect("/")

    if request.method == 'POST':
        # update votes for Secretary
        ScandidateID = request.form.get('S')
        if ScandidateID.isalpha():
            Scandidate = db.execute("SELECT * FROM SHADESvotes WHERE candidateID = :Scandidate_ID", Scandidate_ID = ScandidateID)
        else:
            return redirect("/")
        Scurrent_votes = Scandidate[0]['votes']
        Scurrent_votes += 1
        db.execute("UPDATE SHADESvotes SET votes = :Sc_votes WHERE candidateID = :Scandidate_ID", Sc_votes = Scurrent_votes, Scandidate_ID = ScandidateID)
        # update votes for Joint Secretary
        JScandidateID = request.form.get('JS')
        if JScandidateID.isalpha():
            JScandidate = db.execute("SELECT * FROM SHADESvotes WHERE candidateID = :JScandidate_ID", JScandidate_ID = JScandidateID)
        else:
            return redirect("/")
        JScurrent_votes = JScandidate[0]['votes']
        JScurrent_votes += 1
        db.execute("UPDATE SHADESvotes SET votes = :JSc_votes WHERE candidateID = :JScandidate_ID", JSc_votes = JScurrent_votes, JScandidate_ID = JScandidateID)
        # update votes for Treasurer
        TcandidateID = request.form.get('T')
        if TcandidateID.isalpha():
            Tcandidate = db.execute("SELECT * FROM SHADESvotes WHERE candidateID = :Tcandidate_ID", Tcandidate_ID = TcandidateID)
        else:
            return redirect("/")
        Tcurrent_votes = Tcandidate[0]['votes']
        Tcurrent_votes += 1
        db.execute("UPDATE SHADESvotes SET votes = :Tc_votes WHERE candidateID = :Tcandidate_ID", Tc_votes = Tcurrent_votes, Tcandidate_ID = TcandidateID)
        # logout
        return redirect("/logout")

# logout route
@app.route("/logout")
def logout():
    session.pop('loginID', None)
    session.pop('club', None)
    return render_template("logout.html")

if __name__ == '__main__':
    app.run()