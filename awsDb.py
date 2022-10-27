import random
import mysql.connector,datetime
from datetime import datetime

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

def fetchNameFromAccNo(accNo):
    custId = fetchCustIdFromAccNo(accNo)
    q = '''SELECT CONCAT(CustFirst,' ',CustLast) FROM Customer WHERE CustId=%s'''
    cr.execute(q,[custId])
    return list(cr)[0][0]

def fetchPin(cardNo):
    q = 'SELECT CardPin FROM Card WHERE CardNo='+cardNo
    cr.execute(q)
    return list(cr)[0][0]

def fetchBal(accNo):
    q = 'SELECT AccBal FROM Account WHERE AccNo='+str(accNo)
    cr.execute(q)
    return list(cr)[0][0]

def deductAmount(amount,accNo):
    bal = fetchBal(accNo)
    bal-=int(amount)
    q = 'UPDATE Account SET AccBal='+str(bal)+' WHERE accNo='+str(accNo)
    cr.execute(q)
    mydb.commit()

def fetchMobileFromAccNo(AccNo):
    q='SELECT CustMobile FROM Customer WHERE CustId = '+ str(fetchCustIdFromAccNo(AccNo))
    cr.execute(q)
    return list(cr)[0][0]

def updatePin(cardNO,newPin):
    q = 'UPDATE Card SET cardPin ='+newPin+' WHERE cardNo ='+cardNO
    cr.execute(q)
    mydb.commit()

def connectAtm(hwId):
    q = 'select AtmHwId from Atm;'
    cr.execute(q)
    hwIds = [i[0] for i in cr]
    if hwId[0] in hwIds:
        return
    else:
        q1 = 'alter table Atm auto_increment=1;'
        q = """INSERT INTO `Atm` (`AtmId`, `Atm100`, `Atm200`, `Atm500`, `Atm2000`, `AtmHwId`, `AtmName`) VALUES (
            NULL, NULL, NULL, NULL, NULL, %s, %s);"""
        cr.execute(q1)
        cr.execute(q,hwId)
        mydb.commit()

def genMiniStatement(accNo):
    q = """SELECT TDate,TAmount , CASE
    WHEN TCrAccNo=%s THEN 'Cr'
    ELSE 'Dr' END
    AS TType
    FROM `atm-db`.Transactions where TDrAccNo=%s or TCrAccNo=%s ORDER BY Tid DESC
    LIMIT 5;"""
    cr.execute(q,3*[accNo])
    return list(cr)

def transact(amount,atmId,drAccNo = 'NULL',crAccNo = 'NULL'):
    q1 = 'alter table Transactions auto_increment=1;'
    cr.execute(q1)
    q = """INSERT INTO `Transactions` (`TId`, `TAmount`, `TCrAccNo`, `TDrAccNo`, `TDate`, `TAtmId`) VALUES (NULL, %s, %s, %s, %s, %s);"""
    cr.execute(q,[amount,crAccNo,drAccNo,datetime.date.today(),atmId])
    if drAccNo!='NULL':
        deductAmount(amount,drAccNo)
    if crAccNo!='NULL':
        deductAmount(-int(amount),crAccNo)
    mydb.commit()

def getAtmIdFromHwId(hwId):
    q = '''SELECT AtmId FROM Atm WHERE AtmHwId=%s'''
    cr.execute(q,[hwId])
    return list(cr)[0][0]

def createCust(first ,last ,mob):
    q1 = 'alter table Customer auto_increment=1;'
    cr.execute(q1)
    q = '''INSERT INTO `Customer` (`CustFirst`, `CustLast`, `CustMobile`) VALUES (%s, %s,%s);'''
    cr.execute(q,[first.capitalize(),last.capitalize(),mob])
    mydb.commit()

def insertAc(custId):
    q1 = 'alter table Account auto_increment=1;'
    cr.execute(q1)
    q = '''INSERT INTO `Account` (`CustId`) VALUES (%s);'''
    cr.execute(q,[custId])
    mydb.commit()

def fetchCustIdFromMob(mob:str):
    q = 'SELECT CustId from Customer where CustMobile = '+mob
    cr.execute(q)
    return list(cr)[0][0]    

def fetchLastAc(custId):
    q = 'SELECT AccNo from Account where CustId = '+custId+' ORDER BY AccNo DESC'
    cr.execute(q)
    return list(cr)[0][0] 

def getMobiles():
    q = 'SELECT CustMobile from Customer'
    cr.execute(q)
    return [i[0] for i in list(cr)]

def fetchLastCard(accNo):
    q = 'SELECT CardNo from Card where AccNo = '+accNo
    cr.execute(q)
    return list(cr)[0][0]

def insertCard(accNo,cNet,cType):
    q1 = 'alter table Card auto_increment=4214000000000001;'
    cr.execute(q1)
    exp = int(datetime.today().strftime('%m%y'))+5
    pin = random.randint(1000,9999)
    q = '''INSERT INTO `Card` (`CardExp`, `CardPin`, `AccNo`, `CardNet`, `CardType`) VALUES (%s,%s,%s,%s,%s);'''
    cr.execute(q,[exp,pin,accNo,cNet,cType])
    mydb.commit()
    return fetchLastCard(accNo)

def getAccounts():
    q = 'SELECT AccNo from Account'
    cr.execute(q)
    return [i[0] for i in list(cr)]