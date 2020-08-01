import csv
import passgen
from cs50 import SQL
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
rdb = SQL("sqlite:///JC.db")
db = SQL("sqlite:///project.db")

with open('JC.csv', "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for ID in row:
            loginID = ID
            password = passgen.passgen(length=15, punctuation=False, digits=True, letters=True, case='both')
            hash = bcrypt.generate_password_hash(password)
            rdb.execute("INSERT INTO JCcredentials (loginID, password) VALUES(:login_ID, :pwd)", login_ID = loginID, pwd = password)
            db.execute("INSERT INTO JCID (loginID, password) VALUES(:login_ID, :pwd_hash)", login_ID = loginID, pwd_hash = hash)
