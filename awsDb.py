
import mysql.connector
mydb = mysql.connector.connect(host='atm-db.cl5eytgewt31.ap-south-1.rds.amazonaws.com',
user='admin',
password='velocity',
database='atm-db')

cr = mydb.cursor()

def getCards():
    query = "SELECT CardNo FROM Card"
    cr.execute(query)
    return [i[0] for i in cr]

def fetchAccNoFromCard(cardNo):
    q = 'SELECT AccNo FROM Card WHERE CardNo='+cardNo
    cr.execute(q)
    return list(cr)[0][0]
def fetchCustIdFromAccNo(accNo):
    q = 'SELECT CustId FROM Account WHERE AccNo='+str(accNo)
    cr.execute(q)
    return list(cr)[0][0]

def fetchFirstNameFromCard(cardNo):
    accNo = fetchAccNoFromCard(cardNo)
    custId = fetchCustIdFromAccNo(accNo)
    q = 'SELECT CustFirst FROM Customer WHERE CustId='+str(custId)
    cr.execute(q)
    return list(cr)[0][0]

