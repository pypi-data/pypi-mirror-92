import  extraEncodings
import random
import time
countingstuff = 0
#Gen2
Encodeable_letters = r'''aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ1234567890!@\#$%^&*()`~-=_+[]}{'\";:| ,.<>/?'''
class TwoWayDict(dict):
    def __init__(self, my_dict):
        dict.__init__(self, my_dict)
        self.reverse = {v : k for k,v in my_dict.items()}

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        self.reverse.__setitem__(value, key)

    def pop(self, key):
        self.reverse.pop(self[key])
        dict.pop(self, key)
    def add(self,key,value):
        self.reverse[value] = key
        dict[value] = key
class Encoding():
    '''A way to generate a encoding for your purposes. \n
    Look at CreateAnEncoding.py to see an example of making an instance
    '''
    def __init__(self,rate):
        self.rate = rate
        x = 0
        self.encodingnormal = {}
        for letter in Encodeable_letters:
            x = x + rate
            self.encodingnormal[letter] = str(x)
        self.encoding = TwoWayDict(self.encodingnormal)
    
    def encode(self,obj):
        for character in obj:
            encode = self.encoding[character]
            if character == obj[-1]:
                print(encode,end="\n")
            else:
                print(encode,end=" ")
    
    def decode(self,obj):
        objspce = obj.count(" ") + 1
        obj = obj.split(" ")
        for r in range(objspce):
            de = obj[r]
            decode = self.encoding.reverse[de]
            if de == obj[-1]:
                print(decode,end="\n")
            else:
                print(decode,end="")
    def findrate(self):
        print(f'Rate of {self} is {self.rate}')
        for k,v in self.encoding.reverse.items():
            print(f'{k}:{v}',end='  ')
class ListEncoding():
    def __init__(self,mix):
        self.encoding = []
        self.mix = mix
        for letter in Encodeable_letters:
            self.encoding.append(letter)
    def code(self,Character_to_decode):
        Character_to_decode = str(Character_to_decode)
        for character in Character_to_decode:
            charpos = self.encoding.index(character)
            ResultStr = str(self.encoding[-charpos  -self.mix])
            print(ResultStr,end='')
class RandomEncoding(Encoding):
    '''A way to generate a random encoding for your purposes. \n
    Encoding and decoding works the same as Encoding() \n
    Look at CreateAnEncoding.py and the Encoding() for an example of how to use it.
    '''
    def __init__(self,MaxRandom,MinRandom):
        self.rate = random.randint(MinRandom,MaxRandom)
        x = 0
        self.encodingnormal = {}
        for letter in Encodeable_letters:
            x = x + self.rate
            self.encodingnormal[letter] = str(x)
        self.encoding = TwoWayDict(self.encodingnormal)
Gen2=[]
GTX2 = []   
ichorrev = {
    "a":"1",
    "A":"2",
    "b":"3",
    "B":"4",
    "c":"5",
    "C":"6",
    "d":"7",
    "D":"8",
    "e":"9",
    "E":"10",
    "f":"11",
    "F":"12",
    "g":"13",
    "G":"14",
    "h":"15",
    "H":"16",
    "i":"17",
    "I":"18",
    "j":"19",
    "J":"20",
    "k":"21",
    "K":"22",
    "l":"23",
    "L":"24",
    "m":"25",
    "M":"26",
    "n":"27",
    "N":"28",
    "o":"29",
    "O":"30",
    "p":"31",
    "P":"32",
    "q":"33",
    "Q":"34",
    "r":"35",
    "R":"36",
    "s":"37",
    "S":"38",
    "t":"39",
    "T":"40",
    "u":"41",
    "U":"42",
    "v":"43",
    "V":"44",
    "w":"45",
    "W":"46",
    "x":"47",
    "X":"48",
    "y":"49",
    "Y":"50",
    "z":"51",
    "Z":"52",
    " ":"53",
    ".":"54",
    "?":"55",
    "!":"56",
    ",":"57",
    ";":"58",
    ":":"59",
    "'":"60",
    '"':"61",
    "@":"62",
    "_":"63",
    "-":"64",
    "[":"64",
    "]":"65",
    "{":"66",
    "}":"67",
    "#":"68",
    "$":"69",
    "%":"70",
    "^":"71",
    "&":"72",
    "*":"73",
    "(":"74"
}
LGC = ListEncoding(-1)
ichor = TwoWayDict(ichorrev)
LTF64 = []
for letter in Encodeable_letters:
    countingstuff = countingstuff + 1
    ichor[letter] = countingstuff
    Gen2.append(letter)
    LTF64.append(letter)
    GTX2.append(letter)
def Gen2Code(Character_to_decode):
    ''' Only use with r-strings due to % and \. Don't mind strange coloration as that is just your text   editor rendering it incorrectly'''
    #make sure this is always a string
    Character_to_decode = str(Character_to_decode)
    for character in Character_to_decode:
        charpos = Gen2.index(character)
        ResultStr = str(Gen2[-charpos])
        print(ResultStr,end='')
def LTF64Code(Character_to_decode):
    '''Only use with r-strings due to % and \. Don't mind strange coloration as that is just your text editor rendering it incorrectly'''
    #make sure this is always a string
    Character_to_decode = str(Character_to_decode)
    for character in Character_to_decode:
        charpos = LTF64.index(character)
        ResultStr = str(LTF64[-charpos -2 ])
        print(ResultStr,end='')
def GTX2Code(Character_to_decode):
    '''Only use with r-strings due to % and \. Don't mind strange coloration as that is just your text editor rendering it incorrectly'''
    #make sure this is always a string
    Character_to_decode = str(Character_to_decode)
    for character in Character_to_decode:
        charpos = GTX2.index(character)
        ResultStr = str(GTX2[-charpos  -2])
        print(ResultStr,end='')
#Example below
#LTF64Code(r'Fire balls')
time.sleep(0.3)
print('Initialization:ciphers.py,Complete')