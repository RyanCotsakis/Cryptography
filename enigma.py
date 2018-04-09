""" enigma - Ryan Cotsakis """

import sys
import codecs
import os
import tkFileDialog
import Tkinter
import getpass
import time

CLEAR_COMMAND = "cls"


def encoder(text, pw_num):
    binary_string = ""
    key = []
    for bitNum in range(7*len(text)):
        if pw_num % (((bitNum+1) % pw_num)+1) < ((bitNum+1) % pw_num) // 2:
            binary_string += "1"
        else:
            binary_string += "0"
        if bitNum % 7 == 6:
            key.append(int(binary_string, 2))
            binary_string = ""
    new_text = ""
    old_text = ""
    for x in range(len(text)):
        char_num = ord(text[x])
        if char_num >= 128:
            char_num = ord("?")
            old_text += "?"
        else:
            old_text += text[x]
        new_num = char_num ^ key[x]
        new_text += chr(new_num)

    return old_text, new_text


def write_to_file(f, text):
    f.seek(0)
    f.write(text)
    f.truncate()


def main():
    print "Select a file, or press 'cancel' to create a new file.\n"
    sys.stdout.flush()
    root = Tkinter.Tk()
    root.withdraw()
    f_name = tkFileDialog.askopenfilename(filetypes=(("Text Document", "*.txt"), ("Microsoft Word Document", "*.docx"),
                                                     ("All Files", "*.*")))
    if f_name == '':
        print "Select a directory for the new file.\n"
        sys.stdout.flush()
        directory = tkFileDialog.askdirectory()
        if directory == '':
            return
        version = 0
        while True:
            try:
                f = open(directory + "/enigma_" + str(version) + ".txt", mode="r")
            except IOError:
                break
            f.close()
            version += 1
        f = open(directory + "/enigma_" + str(version) + ".txt", mode="w")
        f.write("This file was automatically created by enigma.\nReplace this text with your information.")
        f.close()
        return

    else:
        f = codecs.open(f_name, encoding="utf-8", mode="r+")
        original_data = f.read()

        pw = getpass.getpass()

        pw_num = 0
        for char in pw:
            pw_num *= 96
            pw_num += ord(char) % 96

        original_data, new_data = encoder(original_data, pw_num)

        if not (pw in original_data or pw in new_data):
            print "WARNING: The password entered could not be found in the document"
            sys.stdout.flush()
            time.sleep(2)

    print "\nCOMMAND LIST:"
    print "write\t\t-translate text and overwrite the file"
    print "view\t\t-translate text and print it to the screen"
    print "current\t\t-view current text"
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
            write_to_file(f, new_data)
            new_data, original_data = original_data, new_data
            print "Write successful."

        elif command in "exit" and command[0] == "e":
            break

        elif "find" in command or (command in "find" and command[0] == "f"):
            if len(command) > 5:
                query = command[5:].lower()
            else:
                print "Enter query:"
                sys.stdout.flush()
                query = raw_input().lower()
            lines = new_data.splitlines()
            for line in lines:
                if query in line.lower():
                    print line

        elif command in "add" and command[0] == "a":
            print "Enter new line:"
            sys.stdout.flush()
            new_line = raw_input()
            new_data += "\n" + new_line
            garbage, original_data = encoder(new_data, pw_num)
            write_to_file(f, original_data)

        elif command in "view" and command[0] == "v":
            print new_data

        elif command in "current" and command[:2] == "cu":
            print original_data

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
    except IOError:
        pass


if __name__ == '__main__':
    main()
