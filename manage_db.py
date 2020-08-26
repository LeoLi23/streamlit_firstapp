# DB
import sqlite3
conn = sqlite3.connect('userdata.db',check_same_thread=False)
conn2 = sqlite3.connect("result.db",check_same_thread=False)
c = conn.cursor()
c2 = conn2.cursor()
# Functions

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,email TEXT,password TEXT)')

def create_usertable_prediction():
    c2.execute('CREATE TABLE IF NOT EXISTS userstable(Cycle TEXT,Age TEXT,Years_home TEXT,Years_business TEXT,Cashflow TEXT,Collateral TEXT,Loan_amount TEXT,Default_rate TEXT,Suggestion TEXT)')

def add_username(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def add_user_email(email,password):
    c.execute('INSERT INTO userstable(email,password) VALUES (?,?)',(email,password))
    conn.commit()

def add_to_result(Cycle,Age,Years_home,Years_business,Cashflow,Collateral,Loan_amount,Default_rate,Suggestion):
    c2.execute('INSERT INTO userstable(Cycle,Age,Years_home,Years_business,Cashflow,Collateral,Loan_amount,Default_rate,Suggestion) VALUES (?,?,?,?,?,?,?,?,?)',(
        Cycle, Age, Years_home, Years_business, Cashflow, Collateral, Loan_amount, Default_rate,Suggestion
    ))
    conn2.commit()
    
def login_user(username = None,email = None,password = None):
    if username is not None and password is not None and email is None:#use username
        c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
        data = c.fetchall()

    elif email is not None and password is not None and username is None:#use email
        c.execute('SELECT * FROM userstable WHERE email =? AND password = ?',(email,password))
        data = c.fetchall()

    return data

def check_unique(username,email):
    if username is not None:
        c.execute('SELECT username FROM userstable WHERE username=?',(username,))
        result1 = c.fetchone()
        if result1 is not None:
            return False
    else:
        c.execute('SELECT email FROM userstable WHERE email=?',(email,))
        result2 = c.fetchone()
        if result2 is not None:
            return False
    return True

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

if __name__=='__main__':
    create_usertable_prediction()
    add_to_result(12,23,4,4,100000,1000000,200000,0.44,"Recommended")
