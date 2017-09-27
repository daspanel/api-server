import sys
import string
import random
import datetime
#import shortuuid
import re

from .cuid import CuidGenerator

def check_pass(password):
    strength = ['Blank','Very Weak','Weak','Medium','Strong','Very Strong']
    score = 1

    if len(password) < 1:
        return strength[0]
    if len(password) < 4:
        return strength[1]

    if len(password) >=8:
        score = score + 1
    if len(password) >=10:
        score = score + 1
    if re.search('\d+',password):
        score = score + 1
    if re.search('[a-z]',password) and re.search('[A-Z]',password):
        score = score + 1
    if re.search('.,[,!,@,#,$,%,^,&,*,(,),_,~,-,]',password):
        score = score + 1

    return strength[score]


def gen_pass(ucase=5, lcase=5, digits=6, schars=0):
    password = ''
    for i in range(int(ucase)):
        password += string.uppercase[random.randint(0,len(string.uppercase)-1)]
    for i in range(int(lcase)):
        password += string.lowercase[random.randint(0,len(string.lowercase)-1)]
    for i in range(int(digits)):
        password += string.digits[random.randint(0,len(string.digits)-1)]
    for i in range(int(schars)):
        password += string.punctuation[random.randint(0,len(string.punctuation)-1)]

    return ''.join(random.sample(password,len(password)))


class UuidGen(object):
    def __init__(self, service='localhost', port=80, user='', password=''):
        self.service = service
        self.port = port
        self.user = user
        self.password = password

    def gen_uniqid(self, lenght=25):
        genuuid = CuidGenerator()
        suuid = genuuid.cuid()
        return suuid[:int(lenght)]

    def gen_pass(self, ucase=5, lcase=5, digits=6, schars=0):
        password = ''
        for i in range(int(ucase)):
            password += string.uppercase[random.randint(0,len(string.uppercase)-1)]
        for i in range(int(lcase)):
            password += string.lowercase[random.randint(0,len(string.lowercase)-1)]
        for i in range(int(digits)):
            password += string.digits[random.randint(0,len(string.digits)-1)]
        for i in range(int(schars)):
            password += string.punctuation[random.randint(0,len(string.punctuation)-1)]

        return ''.join(random.sample(password,len(password)))


