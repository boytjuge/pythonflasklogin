import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="dapp"
)

mydb.reconnect(attempts=1, delay=0)
mycursor = mydb.cursor(dictionary=True)
class register:
    def insert_user(userobj:dict):
        mydb.connect()
        current_dateTime = datetime.now()
        sql = "INSERT INTO users (`email`, `password`,`creat_date`,`updat_date`,`active`) VALUES (%s, %s, %s, %s, %s) ;"
        val = (userobj['username'], userobj['password'],current_dateTime,current_dateTime,1)
        r = mycursor.execute(sql, val)
        mydb.commit()
        mydb.close()
        return r
    def select_user(userobj:dict):
        mydb.connect()
        mycursor.execute("SELECT email, COUNT(*) FROM users WHERE email = %s GROUP BY email", (userobj['username'],))
        # Add THIS LINE
        results = mycursor.fetchall()
        # gets the number of rows affected by the command executed
        row_count = mycursor.rowcount
        mydb.close()
        return row_count

class login:
    def check_user(userobj:dict):
        mydb.connect()
        mycursor.execute("SELECT email, COUNT(*) FROM users WHERE email = %s and `password` = %s and active =1 GROUP BY email", (userobj['username'],userobj['password'],))
        # Add THIS LINE
        results = mycursor.fetchall()
        # gets the number of rows affected by the command executed
        row_count = mycursor.rowcount
        mydb.close()
        return row_count
        
