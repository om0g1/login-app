from os.path import exists 
import sqlite3

def initialize_db_connection():
    try:
        global con,cur
        if exists("modules/app.db") == True:
            con = sqlite3.connect("modules/local_app.db")
            cur = con.cursor()
            return 1
        else:
            con = sqlite3.connect("modules/local_app.db")
            cur = con.cursor()
            cur.execute("CREATE TABLE user(first_name TEXT,second_name TEXT,username TEXT UNIQUE,age INT,password TEXT, email TEXT UNIQUE, profile_photo BLOB)")
            return 1
    except:
        return 0

def close_db_connection():
    try:
        con.close()
        return 1
    except:
        return 0

def add_user(first_name_ = str,second_name_ = str, username_ = str, age_ =int, password_ = str, email_ = str, profile_photo_ = ""):
    initialize_db_connection()
    try:
        cur.execute("INSERT INTO user (first_name, second_name, username, age, password, email, profile_photo) VALUES (?, ?, ?, ?, ?, ?, ?)",(first_name_,second_name_,username_,age_,password_,email_,profile_photo_))
        con.commit()
        con.close()
        return 1
    except:
        return 0

def del_user(username_,password_):
    initialize_db_connection()
    user_data = {"first_name": "",
                "second_name": "",
                "username":"",
                "age":0,
                "password":"",
                "email":"",
                "profile_photo":""
                }
        
    cur.execute("SELECT first_name,second_name,username,age,password,email FROM user WHERE username = ?",(username_,))
    rows = cur.fetchall()
    if rows != []:
        for row in rows:
            user_data["first_name"] = row[0]
            user_data["second_name"] = row[1]
            user_data["username"] = row[2]
            user_data["age"] = row[3]
            user_data["password"] = row[4]
            user_data["password"] = row[5]

            if password_ == user_data["password"]:
                cur.execute("DELETE FROM user WHERE username = ?",(username_,))
                con.commit()
                con.close()
                return 1
            else:
                con.close()
                return 0
    else:
        return 2

def get_user_details(user_name):
    initialize_db_connection()
    user_data = {"first_name": "",
                "second_name": "",
                "age":0,
                "password":"",
                "email":"",
                "profile_photo":""
                }
        
    cur.execute("SELECT first_name,second_name,username,age,password,email,profile_photo FROM user WHERE username = ?",(user_name,))
    rows = cur.fetchall()
    if rows != []:
        for row in rows:
            user_data["first_name"] = row[0]
            user_data["second_name"] = row[1]
            user_data["username"] = row[2]
            user_data["age"] = row[3]
            user_data["password"] = row[4]
            user_data["email"] = row[5]
            user_data["Profile_photo"] = row[6]
        con.close()
        return user_data
    else:
        con.close()
        return 0
    

def verify_password(operand_ = str, value_ = str, password_ = str):
    initialize_db_connection()
    if user_exists(operand_, value_) == 1:
        data = cur.execute("SELECT password FROM user WHERE "+operand_+" = ?",(value_,)).fetchall()
        for row in data:
            if password_ == row[0]:
                con.close()
                return 1
            else:
                con.close()
                return 0
    else:
        return 2

def update_user_details(operand_,value_,operated_,new_value_,password_,):
    if verify_password(operand_,value_,password_) == 1:
        initialize_db_connection()
        cur.execute("UPDATE user SET "+operated_+" = ? WHERE "+operand_+" = ?",(new_value_,value_,))
        con.commit()
        print("Succesfully updated")
        con.close()
        return 1
    else:
        print("wrong password")
        con.close()
        return 0

def user_exists(operand,value):
    initialize_db_connection()
    cur.execute("SELECT first_name,second_name,username,age,password,email FROM user WHERE "+operand+" = ?",(value,))
    rows = cur.fetchall()
    if rows != []:
        return 1
    else:
        return 0

#example on how to use // didn't update this
#add_user("Person's"," Name","Person's Username",18,"some password","email",1)
#print(get_user_details("person's user name"))
#del_user("user's name","user's password")
#verify_password("username","user's username","user's password")
#update_user_details("username","0m0g1","password","newpassword","somepassword")

