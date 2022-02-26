import random
import getpass
import re
import sys
import time
import json

from signal import signal, SIGINT
from pathlib import Path
from encryption import encryptString, decryptString

def validateEmptyString(str):
    if str == "":
        print ("Invalid Input.\nEmpty string is not allowed")
        sys.exit()

def validateSpaceInStr(str):
    if bool(re.search(r"\s", str)):
        print ("Invalid Input.\nEmail or Password string cannot contain space: [" + str + "]")
        sys.exit()

def validateEmail(emailid):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(regex, emailid)):
        return 1
    else:
        print ("Invalid Input.\nEmail id is not valid: [" + emailid + "]")
        sys.exit()

def validateExistingEmail(emailid,jfile):
    with open(jfile) as data_file:    
        data = json.load(data_file)
    for studentDetails in data['student_details']:
        if (studentDetails['email'] == emailid):
            return 1

def write_json(newData,jfile):
    with open(jfile,'r+') as file:
        existingData = json.load(file)
        existingData["student_details"].append(newData)
        file.seek(0)
        json.dump(existingData, file, indent = 4)

def retrievePwd (emailid, jfile):
    with open(jfile) as data_file:    
        data = json.load(data_file)
    for studentDetails in data['student_details']:
        if (studentDetails['email'] == emailid):
            return studentDetails['passcode']

def handler(signal_received, frame):
    print ("\n" * 2)
    print ("Aaaw! It could have been fun.")
    print ("Ok. I'll exit. Try again when you make up your mind.")
    print ("\n" * 1)
    sys.exit()

if __name__ == '__main__':
    signal(SIGINT, handler)

jsonFilename='data.json'
jFilenameObj = Path(jsonFilename)

print ("\n" * 3)
print ("Identify the task you want to perform")
print ("Create new user ==> 1")
print ("Retrieve existing user passcode ==> 2")
task = input ("Enter your choice [1 / 2]: ")
if (task == ""):
    print ("Unrecognized Choice")
    sys.exit()

try:
    int(task)
except ValueError:
    print ("Unrecognized Choice")
    sys.exit()

#print (task)
print ("\n" * 2)

if (int(task) == 1):
    studentName = input ("Enter your name:")
    studentEmail = input ("Enter your email id:")
    studentPwd = getpass.getpass ("Enter password to store:")
    print ("\n" * 2)
    validateEmptyString(studentName)
    validateEmptyString(studentEmail)
    validateEmptyString(studentPwd)
    validateEmail(studentEmail)
    validateSpaceInStr(studentEmail)
    validateSpaceInStr(studentPwd)
    encryptedPwd = encryptString(studentPwd)
    try:
        jsonFileAbsPath = jFilenameObj.resolve(strict=True)
    except FileNotFoundError:
        jsonString = {"student_details":[{"name":studentName,"email":studentEmail,"passcode":str(encryptedPwd)}]}
        jfile = open(jsonFilename,'w')
        json.dump(jsonString, jfile, indent = 4)
        jfile.close()
        print ("Student db updated successfully")
    else:
        emailExists = validateExistingEmail(studentEmail,jsonFilename)
        if (emailExists == 1):
            print ("Invalid Input.\nEmail ID already exists in database: [" + studentEmail + "]")
            sys.exit()
        jsonString = {
            "name":studentName,
            "email":studentEmail,
            "passcode":str(encryptedPwd)
            }
        write_json(jsonString, jsonFilename)
        print ("Student db updated successfully")
elif (int(task) == 2):
    try:
        jsonFileAbsPath = jFilenameObj.resolve(strict=True)
    except FileNotFoundError:
        print ("Database does not exist.\nCreate users before trying to retrieve.")
        sys.exit()
    studentEmail = input ("Enter email id to retrieve passcode:")
    validateEmptyString(studentEmail)
    validateEmail(studentEmail)
    validateSpaceInStr(studentEmail)
    emailExists = validateExistingEmail(studentEmail,jsonFilename)
    if (emailExists == 1):
        encryptedPasscode = retrievePwd(studentEmail, jsonFilename)
        print ("\n" * 2)
        print ("Retrieved passcode:\n[" + encryptedPasscode + "]")
        print ("\n" * 1)
        print ("Do you want to decode the password and display it here?")
        decryptChoice = input ("Enter your choice [y / n]:")
        if (decryptChoice == "y"):
            decryptedPasscode = decryptString(encryptedPasscode)
            print ("\n" * 2)
            print ("Decrypted Passcode:\n" + decryptedPasscode)
            print ("\n" * 2)
        else:
            print ("Thanks for your time")
            print ("\n" * 2)
    else:
        print ("Given email [" + studentEmail + "] does not exist in db.\nCreate user and try again")
        print ("\n" * 2)
else:
    print ("Unrecognized Choice [" + task + "]")
    print ("\n" * 2)

