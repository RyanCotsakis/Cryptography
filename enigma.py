''' enigma - Ryan Cotsakis '''

import codecs
import os
import getpass
import time

CLEAR_COMMAND = 'clear'


def encoder(text, pw_num):
    binary_string = ''
    key = []
    for bitNum in range(7*len(text)):
        if pw_num % (((bitNum+1) % pw_num)+1) < ((bitNum+1) % pw_num) // 2:
            binary_string += '1'
        else:
            binary_string += '0'
        if bitNum % 7 == 6:
            key.append(int(binary_string, 2))
            binary_string = ''
    new_text = ''
    old_text = ''
    for x in range(len(text)):
        char_num = ord(text[x])
        if char_num >= 128:
            char_num = ord('?')
            old_text += '?'
        else:
            old_text += text[x]
        new_num = char_num ^ key[x]
        new_text += chr(new_num)

    return old_text, new_text


def write_to_file(f, text):
    f.seek(0)
    f.write(text)
    f.truncate()


def help():
    print '\nCOMMAND LIST:'
    print 'write\t\t-translate text and overwrite the file'
    print 'cat\t\t-view current text'
    print 'help\t\t-view this information'
    print 'find\t\t-search for query in translated text'
    print 'add\t\t-append line of text to translated text'
    print 'password\t-print password'
    print 'clear\t\t-clear the output screen'
    print 'q\t\t-close the program\n'


def main():
    f_name = raw_input('Filename: ')

    if f_name == '':
        return

    if '.' not in f_name:
        f_name += '.txt'

    try:
        f = codecs.open(os.path.abspath(f_name), encoding='utf-8', mode='r+')
    except IOError:
        print f_name + ': file not found'
        return

    original_data = f.read()

    pw = getpass.getpass('Password: ')

    if pw == '':
        return

    pw_num = 0
    for char in pw:
        pw_num *= 96
        pw_num += ord(char) % 96

    original_data, new_data = encoder(original_data, pw_num)

    if not (pw in original_data or pw in new_data):
        print 'WARNING: the password entered could not be found in the document'
        raw_input('Press <Enter> to continue')
        f_name += '!'

    help()

    while True:
        command = raw_input('enigma:' + f_name + '$').strip()

        if command == 'write':
            write_to_file(f, new_data)
            new_data, original_data = original_data, new_data
            print 'write successful'

        elif command == 'q':
            break

        elif command[:4] == 'find':
            if len(command) > 5:
                query = command[5:].lower()
            else:
                query = raw_input('Search for: ').lower()
            lines = new_data.splitlines()
            for line in lines:
                if query in line.lower():
                    print line

        elif command[:3] == 'add':
            if len(command) > 4:
                new_line = command[4:]
            else:
                new_line = raw_input('New line: ')
            new_data += '\n' + new_line
            garbage, original_data = encoder(new_data, pw_num)
            write_to_file(f, original_data)

        elif command == 'cat':
            print original_data

        elif command == 'clear':
            os.system(CLEAR_COMMAND)

        elif command == 'help':
            help()

        elif command == 'password':
            print pw
            raw_input('Press <Enter> to continue')
            os.system(CLEAR_COMMAND)

        elif not command == '':
            print command + ': command not found'

    try:
        f.close()
    except IOError:
        pass


if __name__ == '__main__':
    main()
