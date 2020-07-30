import csv
# replace with your choice of module
import password_generator 
from cs50 import SQL
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
rdb = SQL("sqlite:///raw.db")
db = SQL("sqlite:///database.db")

with open('voter_list.csv', "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for email in row:
            emailID = email
            for i in range(len(emailID)):
                if emailID[i] == '@':
                    break
            loginID = emailID[:i]
            password = password_generator.generate()
            pw_hash = bcrypt.generate_password_hash(password)
            rdb.execute("INSERT INTO raw (loginID, emailID, password, hash) VALUES(:login, :email, :pwd, :hash)", login=loginID, email=emailID, pwd=password, hash = pw_hash)
            db.execute("INSERT INTO credentials (loginID, password) VALUES(:ID, :password)", ID=loginID, password=pw_hash)    
