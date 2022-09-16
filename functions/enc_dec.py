import os
import string
import  random

def encrypt(str,r):
    asc = string.ascii_letters+"@ 1234567890.+-*/<>?;:{[]}=_()&^%$#!~`,'"
    if(asc.index(str)+r>len(asc)-1):
        return asc[asc.index(str)+r-len(asc)]
    else:
        return asc[asc.index(str)+r]

def decrypt(str,r):
    asc = string.ascii_letters+"@ 1234567890.+-*/<>?;:{[]}=_()&^%$#!~`,'"
    return asc[asc.index(str)-r]



def encryptfile(f):
    file=open(f,"r")
    arr=f.split('.txt')
    temp=f
    f=arr[-2]
    encfile=open(f+"_enc.txt","a")
    encfile.truncate(0)
    keyfile=open(f+".key","a")
    keyfile.truncate(0)
    for j in file:
        str_ori=j
        enc=""
        key=[]

        for i in str_ori:
            if i=="\n":
                break
            r=random.randint(0,91)
            enc+=encrypt(i,r)
            key.append(r)
        for k in range(0,len(key)):
            if k==len(key)-1:
                keyfile.write(str(key[k])+"\n")
            else:
                keyfile.write(str(key[k]) + " ")

        encfile.write(enc+"\n")
    file.close()
    encfile.close()
    keyfile.close()
    os.remove(temp)
def decryptfile(f,k):
    encfile=open(f,"r")
    arr=k.split('.key')
    temp=f
    f=arr[-2]
    decfile = open(f+".txt", "a")
    keyfile = open(k, "r")
    for str in encfile:
        for keystr in keyfile:
            key=keystr.split()
            dec=""
            for i in range(len(key)):
                dec+=decrypt(str[i],int(key[i]))
            decfile.write(dec+"\n")
            break
    decfile.close()
    keyfile.close()
    encfile.close()
    os.remove(temp)
    os.remove(k)



