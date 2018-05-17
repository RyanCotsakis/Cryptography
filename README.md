# enigma - Ryan Cotsakis
### Encrypt your sensitive documents

##### COMMAND LIST:
- **add []** append line of text to translated text'
- **cat** view current text'
- **clear** clear the output screen'
- **find []** search for query in translated text'
- **help** view this information'
- **password** print password'
- **q(uit)** close the program'
- **write** translate text and overwrite the file\n'

### Linux Installation
1. Download "enigma.py"
2. Edit "~/.bashrc" by appending
  `alias enigma='function _enigma(){ python <Path to enigma.py> $1; };_enigma'`
  to the end of the file.
3. Then open a new terminal window and run:
  `. ~/.bashrc`
  `enigma <filename>`