import random
import string

def generateRandomString(numChars):
    characters = string.ascii_letters + string.punctuation + string.digits + string.punctuation
    randomCharacters = ""
    for i in range(numChars):
        randomCharacters += random.choice(characters)
    return randomCharacters

def encryptString(string):
    key = random.randint(3,9)
    encryptedString = str(key) + generateRandomString(key)
    for i in string:
        encryptedString += i + generateRandomString(key)
    return encryptedString
	
def decryptString(string):
    key = int(string[0]) 
    startPos = 1+key
    stringLen = len(string)
    decryptedString = ""
    for i in range(startPos, stringLen, key+1):
        decryptedString += string[i]
    return decryptedString


#rawString = "hello" #getpass.getpass("Enter text to encrypt: ")
#encryptionKey = random.randint(3,9)

#encryptedOutput = encryptString(rawString, encryptionKey)
#print ("encrypted string: " + encryptedOutput + "\nKey: " + str(encryptionKey))

#decryptedOutput = decryptString(encryptedOutput)
#print ("Decrypted string: " + decryptedOutput)
