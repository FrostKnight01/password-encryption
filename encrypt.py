import random
import string
import getpass



def randString(num):
	randChar = ""
	for i in range(num):
		randChar += random.choice(characters)
	return randChar


def encryptStr(string, val):
	encrypted_string = str(val) + randString(val)
	for i in string:
		encrypted_string += i + randString(val)
	return encrypted_string
	
def decryptStr(string):
	key = int(string[0]) 
	startVal = 1+key
	strLen = len(string)
	decrypted_string = ""
	for i in range(startVal, strLen, key+1):
		decrypted_string += string[i]
	return decrypted_string





characters = string.ascii_letters + string.punctuation + string.digits
string_to_encrypt = getpass.getpass("Enter text to encrypt: ")
encVal = 5

# print (characters)

encrypted_output = encryptStr(string_to_encrypt, encVal)
print ("encrypted string: " + encrypted_output)

input()
user_input = input("Do you want the program to decrypt and show your input?(y/n) \n")

if user_input.casefold() == "y":
	decrypted_output = decryptStr(encrypted_output)
	print ("Your string input is: " + decrypted_output)
elif user_input.casefold() == "n":
	print ("wise choice, I am not disclosing your input")
else:
	print("I did not understand your input. Try again")