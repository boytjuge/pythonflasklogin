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
        

class product:
    def product_all():
        return 1


class product_type:
    def all_type():
        mydb.connect()
        mycursor.execute("SELECT uid, type_name ,type_name_local FROM type WHERE active = 1")
        # Add THIS LINE
        results = mycursor.fetchall()
        mydb.close()
        return results
        
    def product_byTypeId(uid):
        mydb.connect()
        mycursor.execute(f"SELECT 	products.uid,	products.product_name,	products.product_detail,	products.product_price,	products.product_coupong,	products.product_img,products.type_uid,	products.iscoupong,	products.active ,	coupong_sale.discount,	coupong_sale.unit,	CASE WHEN products.iscoupong =  'Y'  AND coupong_sale.unit ='percent' THEN	products.product_price  - ( coupong_sale.discount /100 )	WHEN products.iscoupong =  'Y'  AND coupong_sale.unit ='bath' THEN		products.product_price  -  coupong_sale.discount 	ELSE		products.product_price	END  as SaleDiscount ,product_unit.`unit_local` FROM	products 	left join coupong_sale on coupong_sale.`uid` = products.`product_coupong`  and coupong_sale.active = 1 LEFT JOIN product_unit on product_unit.uid = products.unit_uid  and product_unit.active= 1 WHERE	products.type_uid = {uid} AND products.active = 1")
        # Add THIS LINE
        results = mycursor.fetchall()
        mydb.close()
        return results
