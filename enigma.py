""" enigma - Ryan Cotsakis """

import sys
import codecs
import os
import tkFileDialog
import Tkinter
import getpass
import time

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

def main():
	print "Select a file, or press 'cancel' to create a new file.\n"
	sys.stdout.flush()
	root = Tkinter.Tk()
	root.withdraw()
	fname = tkFileDialog.askopenfilename(filetypes = (("Text Document","*.txt"),("Microsoft Word Document","*.docx"),("All Files","*.*")))
	if fname == '':
		print "Select a directory for the new file.\n"
		sys.stdout.flush()
		directory = tkFileDialog.askdirectory()
		if directory == '':
			return
		version = 0
		while True:
			try:
				f = open(directory + "/enigma_" + str(version) + ".txt", mode = "r")
			except:
				break
			f.close()
			version += 1
		f = open(directory + "/enigma_" + str(version) + ".txt", mode = "w")
		f.write("This file was automatically created by enigma.\nReplace this text with your information.")
		f.close()
		return
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

		if command in "write" and command[0] == "w":
			write_to_file(f,newData)
			newData, originalData = originalData, newData
			print "Write to file successful. Type 'current' to view the new contents."

		elif command in "exit" and command[0] == "e":
			break

		elif "find" in command or (command in "find" and command[0] == "f"):
			if len(command) > 5:
				query = command[5:].lower()
			else:
				print "Enter query:"
				sys.stdout.flush()
				query = raw_input().lower()
			lines = newData.splitlines()
			for line in lines:
				if query in line.lower():
					print line

		elif command in "add" and command[0] == "a":
			print "Enter new line:"
			sys.stdout.flush()
			newLine = raw_input()
			newData += "\n" + newLine
			garbage, originalData = encoder(newData, pwNum)
			write_to_file(f,originalData)

		elif command in "view" and command[0] == "v":
			print newData

		elif command in "current" and command[:2] == "cu":
			print originalData

		elif command in "clear" and command[:2] == "cl":
			os.system(CLEAR_COMMAND)

		elif command in "password" and command[0] == "p":
			print pw
			time.sleep(2)
			os.system(CLEAR_COMMAND)

		else:
			print "Invalid command, " + command

	try:
		f.close()
	except:
		pass

if __name__ == '__main__':
	main()











