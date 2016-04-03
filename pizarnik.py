"""
Collate pyzarnik.xml
David J. Birnbaum (djbpitt@gmail.com)
First version: 2016-03-27

Pull parser code lightly adapted from Ronald Haentjens Dekker's
    https://github.com/rhdekker/python_xml_pull_parser_example/blob/master/pull_parser_test.py
"""
import sys
import re
from xml.dom.minidom import Element, Text
from xml.dom.pulldom import CHARACTERS, START_ELEMENT, parseString, END_ELEMENT

# Use djb development version of collatex (https://github.com/djbpitt/collatex, "experimental" branch)
sys.path.append('/Users/djb/collatex/collatex-pythonport/')
from collatex import *

class Stack(list):
    def push(self, item):
        self.append(item)

    def peek(self):
        return self[-1]

# Initialize input and output
source = open('pizarnik.xml','r').read()
doc = parseString(source)
witnesses = {}

# Only process content inside witnesses
inWitness = False
inLine = False

# Tokenize, keeping leading whitespace (whitespace after last token is processed separately)
def tokenize(contents):
    return re.findall(r'\s*\S+', contents)

# Regex
startWhite = re.compile(r'\s+') # strip leading whitespace; match() is automatically anchored at the start
endWhite = re.compile(r'\S\s+$') # test for trailing whitespace to include in output

for event, node in doc:
    if event == START_ELEMENT and node.tagName == 'version':
        # create dictionary entry: key = @wit identifier and value = list of tokens
        inWitness = True
        witnesses[node.getAttribute('wit')] = Stack()
        currentWitness = witnesses[node.getAttribute('wit')]
        currentWitness.push(Element('reading'))
    elif not inWitness:
        # ignore events not inside a witness
        continue
    elif event == END_ELEMENT and node.tagName == 'version':
        inWitness = False
    # Events below here fire only in inside witness
    elif event == START_ELEMENT:
        # <l> elements are not flattened; all others are
        if node.tagName == 'l':
            inLine = True
            t = Text()
            t.data = '\n'
            currentWitness.peek().appendChild(t)
            currentWitness.peek().appendChild(node)
            currentWitness.push(node)
        elif not inLine:
            continue
        else:
            node.setAttribute('type', 'start')
            currentWitness.peek().appendChild(node)
    elif event == END_ELEMENT:
        # Create matching empty "end" element for any element except <l>
        if node.tagName == 'l':
            inLine = False
            currentWitness.pop()
        elif not inLine:
            continue
        else:
            clone = node.cloneNode(False)
            clone.setAttribute('type', 'end')
            currentWitness.peek().appendChild(clone)
    elif event == CHARACTERS:
        if not inLine:
            continue
        else:
            # tokens have optional leading whitespace
            tokens = tokenize(node.data)
            textdata = ''
            for token in tokens:
                if startWhite.match(token):
                    # if there's leading whitespace replace it with a new line
                    textdata += '\n'
                textdata += startWhite.sub('',token)
            if endWhite.search(node.data):
                # if there was whitespace at the end of character data, output a new line
                textdata += '\n'
            t = Text()
            t.data = textdata
            currentWitness.peek().appendChild(t)
for key, value in witnesses.items():
    print(value.pop().toxml())
