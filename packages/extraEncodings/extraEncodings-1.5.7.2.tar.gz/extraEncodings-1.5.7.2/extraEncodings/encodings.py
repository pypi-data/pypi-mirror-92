#imports
import os
import time
import  extraEncodings.ciphers
from  extraEncodings.ciphers import *
import  extraEncodings.encodingsGui
from extraEncodings.encodingsGui import *
print('Initialization:encodings.py,Complete')
#functions to encode and decode
def encodeto():
    entype = input("Which encoding?")
    if entype.upper() == "ichor".upper():
        obj = input("Encode:")
        for character in obj:
            encode = ichor[character]
            if character == obj[-1]:
                print(encode,end="\n")
            else:
                print(encode,end=" ")
    if entype.upper() == "GEN2":
        Gen2Code(input('Encode:'))
    if entype.upper() == 'LTF64':
        LTF64Code(input('Encode:'))
    if entype.upper() == 'GTX2':
        GTX2Code(input('Decode '))
    if entype.upper() == 'LGC':
        LGC.code(input('Encode'))

def decodeto():
    detype = input("Which decoding?")
    if detype.upper() == "ichor".upper():
        obj = input("Decode:")
        objspce = obj.count(" ") + 1
        obj = obj.split(" ")
        for r in range(objspce):
            de = int(obj[r])
            decode = ichor.reverse[de]
            if de == obj[-1]:
                print(decode,end="\n")
            else:
                print(decode,end="")
    if detype.upper() == "GEN2":
        Gen2Code(input('Decode:'))
    if detype.upper() == 'LTF64':
        LTF64Code(input('Decode:'))
    if detype.upper() == 'GTX2':
        GTX2Code(input('Decode '))
    if detype.upper() == 'LGC':
        LGC.code(input('Decode'))
def clear():
    ostype = os.name
    if ostype.upper() == 'posix'.upper():
        os.system('clear')
    if ostype.upper() == 'nt'.upper():
        os.system('cls')




#while true loop for coder
def coder():
    x = ""
    clear()
    while x != "exit".upper():
        x = input("\nEncode, Decode, Clear, Credits, GUI , or exit?:")
        x = x.upper()
        if x == "encode".upper():
            encodeto()
        if x == "decode".upper():
            decodeto()
        if x  == "Credits".upper():
            print("Everything: code80191@gmail.com")
            time.sleep(1)
        if x == "clear".upper():
            clear()
        if x == "GUI".upper():
            startGUI()
        if  x == "secrets".upper():
            print(''':>9~;9cW;5C:/9~;9cCW;5C:/9~;9''')
time.sleep(0.5)
print('Initialization:encodings.py,Complete')
print('Finshed!')
time.sleep(2)
if __name__ == "__main__":
    coder()
