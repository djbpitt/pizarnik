import re
from xml.dom.minidom import Element, Text
from xml.dom.pulldom import CHARACTERS, START_ELEMENT, parseString, END_ELEMENT

"""
 XML pull parser and minidom demo
 @author: Ronald Haentjens Dekker
"""


class Stack(list):
    def push(self, item):
        self.append(item)

    def peek(self):
        return self[-1]


def tokenize(contents):
    return re.findall("[.?!,;:]+[\\s]*|[^.?!,;:\\s]+[\\s]*", contents)

source = """<rdg wit="#ipa">рускаꙗ землѧ <lb/>
                                <add place="margin">и хто в неи почалъ пѣрвѣе кнѧжи<hi rend="sup"
                                        >т</hi></add>·:·</rdg>"""
# init input
doc = parseString(source)

# init output
output = Element("output")
open_elements = Stack()
open_elements.push(output)

for event, node in doc:
    # debug
    # print(event, node)
    if event == START_ELEMENT:
        # skip rdg element
        if node.localName == "rdg":
            continue
        # in case of add deal with overlapping hierarchies
        if node.localName == "add":
            # set type attribute to start and add node as a child to output
            node.setAttribute("type","start")
            open_elements.peek().appendChild(node)
        else:
            open_elements.peek().appendChild(node)
            open_elements.push(node)
    elif event == END_ELEMENT:
        # skip rdg element
        if node.localName == "rdg":
            continue
        # in case of add deal with overlapping hierarchies
        if node.localName == "add":
            # create a clone of the node and set type attribute to end and add node as a child to output
            clone = node.cloneNode(False)
            clone.setAttribute("type","end")
            open_elements.peek().appendChild(clone)
        else:
            open_elements.pop()
    elif event == CHARACTERS:
        tokens = tokenize(node.data)
        if tokens:
            textdata = "\n".join(tokens)
        else:
            textdata = re.sub("[^\S\n]+", "", node.data)
        t = Text()
        t.data = textdata
        open_elements.peek().appendChild(t)

print(output.toxml())