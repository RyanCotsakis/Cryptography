""" PASSWORD DECODER - Ryan Cotsakis """

import sys
import codecs
import os
import tkFileDialog
import Tkinter

CLEAR_COMMAND = "cls"

def encoder(text,pwNum):
	binStr = ""
	key = []
	for bitNum in range(7*len(text)):
		if pwNum%(((bitNum+1)%pwNum)+1) < ((bitNum+1)%pwNum)//2:
			binStr += "1"
		else:
			binStr += "0"
		if bitNum % 7 == 6:
			key.append(int(binStr,2))
			binStr = ""
	newtext = ""
	for x in range(len(text)):
		newNum = ord(text[x]) ^ key[x]
		newtext += chr(newNum)
	return newtext

print "Select a file.\n"
sys.stdout.flush()
root = Tkinter.Tk()
root.withdraw()
fname = tkFileDialog.askopenfilename(filetypes = (("Text Document","*.txt"),("All Files","*.*")))
f = codecs.open(fname, encoding = "utf-8", mode = "r+")

print "Enter password:"
sys.stdout.flush()
pw = raw_input()
os.system(CLEAR_COMMAND)
pwNum = 0
for char in pw:
	pwNum *= 96
	pwNum += ord(char)%96

originalData = f.read()
newData = encoder(originalData,pwNum)

print "COMMAND LIST:"
print "view\t\t-translate text"
print "current\t\t-view current text"
print "write\t\t-write translated text to file"
print "find\t\t-search for query in translated text"
print "add\t\t-append line of text to translated text"
print "password\t-print password"
print "hide\t\t-clear the output screen"
print "exit\t\t-close program"

while True:
	print "\nEnter command:"
	sys.stdout.flush()
	command = raw_input().strip()

	if command == "write":
		f.seek(0)
		f.write(newData)
		f.truncate()
		newData, originalData = originalData, newData

	elif command == "exit":
		break

	elif command == "find":
		print "Enter query:"
		sys.stdout.flush()
		query = raw_input().lower()
		lines = newData.splitlines()
		for line in lines:
			if query in line.lower():
				print line

	elif command == "add":
		print "Enter new line:"
		sys.stdout.flush()
		newLine = raw_input()
		newData += "\n" + newLine
		originalData = encoder(newData, pwNum)
		f.seek(0)
		f.write(originalData)
		f.truncate()

	elif command == "view":
		print newData

	elif command == "current":
		print originalData

	elif command == "hide":
		os.system(CLEAR_COMMAND)

	elif command == "password":
		print pw

	else:
		print "Invalid command, " + command











