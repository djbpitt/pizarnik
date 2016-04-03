"""
Collate pyzarnik_etree.xml
David J. Birnbaum (djbpitt@gmail.com)
First version: 2016-04-02
"""
import sys
import re
import json
from lxml import etree

# Use djb development version of collatex (https://github.com/djbpitt/collatex, "experimental" branch)
sys.path.append('/Users/djb/collatex/collatex-pythonport/')
from collatex import *

class Witness:
    def __init__(self,witness):
        self.witness = witness
        self.xml = etree.XML(self.witness)
        self.siglum = self.xml.attrib['wit']
        self.lines = [Line(line) for line in self.xml.findall('.//l')]
    def __len__(self):
        return len(self.lines)
    def __getitem__(self,key):
        return self.lines[key]

class Line:
    """An instance of Line is a line in a witness, expressed as an <l> element"""
    addWMilestones = etree.XML("""
    <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
        <xsl:output method="xml" indent="no" encoding="UTF-8" omit-xml-declaration="yes"/>
        <xsl:template match="*|@*">
            <xsl:copy>
                <xsl:apply-templates select="node() | @*"/>
            </xsl:copy>
        </xsl:template>
        <xsl:template match="/*">
            <xsl:copy>
                <xsl:apply-templates select="@*"/>
                <!-- insert a <w/> milestone before the first word -->
                <w/>
                <xsl:apply-templates/>
            </xsl:copy>
        </xsl:template>
        <!-- convert <add>, <sic>, and <crease> to milestones (and leave them that way)
             CUSTOMIZE HERE: add other elements that may span multiple word tokens
        -->
        <xsl:template match="add | del | gap ">
            <xsl:element name="{name()}">
                <xsl:attribute name="n">start</xsl:attribute>
                <xsl:copy-of select="@*"/>
            </xsl:element>
            <xsl:apply-templates/>
            <xsl:element name="{name()}">
                <xsl:attribute name="n">end</xsl:attribute>
            </xsl:element>
        </xsl:template>
        <xsl:template match="note"/>
        <xsl:template match="text()">
            <xsl:call-template name="whiteSpace">
                <xsl:with-param name="input" select="translate(.,'&#x0a;',' ')"/>
            </xsl:call-template>
        </xsl:template>
        <xsl:template name="whiteSpace">
            <xsl:param name="input"/>
            <xsl:choose>
                <xsl:when test="not(contains($input, ' '))">
                    <xsl:value-of select="$input"/>
                </xsl:when>
                <xsl:when test="starts-with($input,'  ')">
                    <xsl:call-template name="whiteSpace">
                        <xsl:with-param name="input" select="substring($input,2)"/>
                    </xsl:call-template>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="substring-before($input, ' ')"/>
                    <w/>
                    <xsl:call-template name="whiteSpace">
                        <xsl:with-param name="input" select="substring-after($input,' ')"/>
                    </xsl:call-template>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:template>
    </xsl:stylesheet>
    """)
    transformAddW = etree.XSLT(addWMilestones)
    xsltWrapW = etree.XML('''
    <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
        <xsl:output method="xml" indent="no" omit-xml-declaration="yes"/>
        <xsl:template match="/*">
            <xsl:copy>
                <xsl:apply-templates select="w"/>
            </xsl:copy>
        </xsl:template>
        <xsl:template match="w">
            <!-- faking <xsl:for-each-group> as well as the "<<" and except" operators -->
            <xsl:variable name="tooFar" select="following-sibling::w[1] | following-sibling::w[1]/following::node()"/>
            <w>
                <xsl:copy-of select="following-sibling::node()[count(. | $tooFar) != count($tooFar)]"/>
            </w>
        </xsl:template>
    </xsl:stylesheet>
    ''')
    transformWrapW = etree.XSLT(xsltWrapW)
    def __init__(self,line):
        self.line = line
    def tokens(self):
        return [Word(token).createToken() for token in Line.transformWrapW(Line.transformAddW(self.line)).xpath('//w')]

class Word:
    unwrapRegex = re.compile('<w>(.*)</w>')
    stripTagsRegex = re.compile('<.*?>')

    def __init__(self, word):
        self.word = word

    def unwrap(self):
        return Word.unwrapRegex.match(etree.tostring(self.word, encoding='unicode')).group(1)

    def normalize(self):
        return Word.stripTagsRegex.sub('', self.unwrap().lower())

    def createToken(self):
        token = {}
        token['t'] = self.unwrap()
        token['n'] = self.normalize()
        return token

tree = etree.parse('pizarnik.xml')
root = tree.getroot()
versions = root.findall('.//version')
versionSet = [Witness(etree.tostring(version)) for version in versions]
lineCount = len(versionSet[0]) # 9 lines
for lineNo in range(lineCount):
    json_input = {}
    witnesses = []
    json_input["witnesses"] = witnesses
    for versionNo in range(len(versionSet)):
        witnessData = {}
        witnessData["id"] = versionSet[versionNo].siglum
        witnessData["tokens"] = Line(versionSet[versionNo].lines[lineNo]).line.tokens()
        witnesses.append(witnessData)
    # print(json.dumps(json_input))
    collation = collate(json_input, output='json')
    print(collation)
