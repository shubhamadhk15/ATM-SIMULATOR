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
    bal-=amount
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