'''Author :: Ankit Yadav
    Date :: 14/09/2022
'''
import os,enc_dec,subprocess
from zipfile import ZipFile
from awsDb import *

def generate_card(card_no,name):   #generates a card file 'name.card' for card_no in the working directory

    with open('temp.txt','w') as f:
        f.write(card_no)
    enc_dec.encryptfile('temp.txt')

    with ZipFile(name+'.card','w') as z:
        z.write('temp_enc.txt')
        z.write('temp.key')
    os.remove('temp_enc.txt')
    os.remove('temp.key')

def fetch_card(card):
    with ZipFile(card,'r') as z:
        z.extractall()
    enc_dec.decryptfile('temp_enc.txt','temp.key')
    with open('temp.txt','r') as f2:
        val = f2.read()
    os.remove('temp.txt')
    return val[:len(val)-1]

def isValidCardNo(cardNo):
    cardList = getCards()
    if cardNo in cardList:
        return True
    else:
        return False

def cssLoader(file):
    with open(file,'r') as f:
        rd = f.read()
    return rd

def getHwId():
    current_machine_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
    return current_machine_id,os.getlogin()
