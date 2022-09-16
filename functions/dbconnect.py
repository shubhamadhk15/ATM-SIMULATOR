
import mysql.connector
mydb = mysql.connector.connect(
    host = 'sql6.freesqldatabase.com',
    user = 'sql6519540',
    password = 'AgskhzyAFS',
    database = 'sql6519540'
)


cr = mydb.cursor()
query = "SELECT Cust_FirstName FROM Customer WHERE Cust_FirstName = 'Ankit'"
cr.execute(query) 
print(list(cr)[0][0])