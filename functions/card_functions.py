'''Author :: Ankit Yadav
    Date :: 14/09/2022
'''

import enc_dec,os
from zipfile import ZipFile

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
    os.remove(card)
    enc_dec.decryptfile('temp_enc.txt','temp.key')
    with open('temp.txt','r') as f2:
        val = f2.read()
    os.remove('temp.txt')
    return val

generate_card('1258965482','AnkitYadav')