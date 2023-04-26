import mysql.connector as mysql

MYSQL_USER =  'root' #replace with your user name.
MYSQL_PASS =  'elin2020' #replace with your MySQL server password
MYSQL_DATABASE = 'samir'#replace with your database name

connection = mysql.connect(user=MYSQL_USER,
                           passwd=MYSQL_PASS,
                           database=MYSQL_DATABASE, 
                           host='127.0.0.1')


cnx = connection.cursor(dictionary=True)
cnx.execute('''DROP TABLE IF EXISTS Names''')
cnx.execute('''CREATE TABLE Names (name varchar(20))''')
cnx.execute('''INSERT INTO Names VALUES ('test')''')
cnx.execute('''INSERT INTO Names VALUES ('test_1')''')
cnx.execute('''SELECT * FROM Names''')


for row in cnx:
    print(row)
connection.close()

