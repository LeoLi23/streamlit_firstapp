# DB
import sqlite3
conn = sqlite3.connect('userdata.db',check_same_thread=False)
c = conn.cursor()

# Functions

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,email TEXT,password TEXT)')


def add_username(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def add_user_email(email,password):
    c.execute('INSERT INTO userstable(email,password) VALUES (?,?)',(email,password))
    conn.commit()

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
    create_usertable()
    print(login_user(username = 'leo',password = 1234))
    print(login_user(email = 'leo23@gmail.com',password =1234 ))
    #add_userdata('Leo',,12345)
    #check_unique('Leo','123@gmail.com')
