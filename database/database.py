import csv
import passgen
from cs50 import SQL
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
rdb = SQL("sqlite:///database.db")
db = SQL("sqlite:///project.db")

with open('voter_list.csv', "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for email in row:
            emailID = email
            for i in range(len(emailID)):
                if emailID[i] == '@':
                    break
            loginID = emailID[:i]
            password = passgen.passgen(length=15, punctuation=True, digits=True, letters=True, case='both')
            pw_hash = bcrypt.generate_password_hash(password)
            rdb.execute("INSERT INTO raw (loginID, emailID, password, hash) VALUES(:login, :email, :pwd, :hash)", login=loginID, email=emailID, pwd=password, hash = pw_hash)
            db.execute("INSERT INTO credentials (loginID, password) VALUES(:ID, :password)", ID=loginID, password=pw_hash)    