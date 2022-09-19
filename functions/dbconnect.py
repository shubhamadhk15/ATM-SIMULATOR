
import mysql.connector
mydb = mysql.connector.connect(
    host = 'sql6.freesqldatabase.com',
    user = 'sql6519540',
    password = 'AgskhzyAFS',
    database = 'sql6519540'
)


cr = mydb.cursor()
query = "INSERT INTO `Account` (`Acc_Bal`, `Cust_Id`) VALUES ('100000', '2');"
cr.execute(query) 
# for i in cr:
#     print(i)

mydb.commit()