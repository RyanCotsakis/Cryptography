""" enigma - Ryan Cotsakis """

import sys
import codecs
import os
import tkFileDialog
import Tkinter
import getpass
from docx import Document

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
	oldtext = ""
	for x in range(len(text)):
		charNum = ord(text[x])
		if charNum >= 128:
			charNum = ord("?")
			oldtext += "?"
		else:
			oldtext += text[x]
		newNum = charNum ^ key[x]
		newtext += chr(newNum)

	return oldtext, newtext

def write_to_file(file,text):
	file.seek(0)
	file.write(text)
	file.truncate()

print "Select a file.\n"
sys.stdout.flush()
root = Tkinter.Tk()
root.withdraw()
fname = tkFileDialog.askopenfilename(filetypes = (("Text Document","*.txt"),("Microsoft Word Document","*.docx"),("All Files","*.*")))
fex = fname.split(".")
if "doc" in fex[1]:
	document = Document(fname)
	f = codecs.open(fex[0] + ".txt", encoding = "utf-8", mode = "w")
	f.write("This file was created automatically by encoder_1.1")
	f.flush()
	originalData = ""
	for p in document.paragraphs:
		originalData += p.text + "\n"
else:
	f = codecs.open(fname, encoding = "utf-8", mode = "r+")
	originalData = f.read()

pw = getpass.getpass()

pwNum = 0
for char in pw:
	pwNum *= 96
	pwNum += ord(char)%96

originalData, newData = encoder(originalData,pwNum)

print "\nCOMMAND LIST:"
print "view\t\t-translate text"
print "current\t\t-view current text"
print "write\t\t-write translated text to file"
print "find\t\t-search for query in translated text"
print "add\t\t-append line of text to translated text"
print "password\t-print password"
print "clear\t\t-clear the output screen"
print "exit\t\t-close program"

while True: 
	print "\nEnter command:"
	sys.stdout.flush()
	command = raw_input().strip()

	if command == "write":
		write_to_file(f,newData)
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
		garbage, originalData = encoder(newData, pwNum)
		write_to_file(f,originalData)

	elif command == "view":
		print newData

	elif command == "current":
		print originalData

	elif command == "clear":
		os.system(CLEAR_COMMAND)

	elif command == "password":
		print pw

	else:
		print "Invalid command, " + command











