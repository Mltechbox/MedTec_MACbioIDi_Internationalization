'''
Created on 20 june 2017

@author: marilola.afonso@ulpgc.com
@organization: MACbioIDi
@version: 0.0 for NAMIC 25th Project Week. Summer 2017
'''

import xml.etree.ElementTree as ET


class mdasLiteral:
    def __init__(self, module):
        self.module = module
        self.path = '../language/language.xml'
        self.getLanguage(self)

    # Define our CDATA node
    def CDATA(self, text=None):
        element = ET.Element('![CDATA[')
        element.text = text
        return element

    # Overwrite serialize
    ET._original_serialize_xml = ET._serialize_xml

    def _serialize_xml(write, elem, qnames, namespaces, short_empty_elements):
        if elem.tag == '![CDATA[':
            write("<%s%s]]>" % (elem.tag, elem.text))
            return
        return ET._original_serialize_xml(write, elem, qnames, namespaces,short_empty_elements)

    ET._serialize_xml = ET._serialize['xml'] = _serialize_xml
    # END Overwrite serialize

    @staticmethod

    def getLanguage(self):
        doc = ET.parse(self.path)
        root = doc.getroot()
        self.default = root.find('default').text
        
        if (root.find('last').text):
            self.language = root.find('last').text
        else:
            self.language = self.default
        return self.language

    def getLanguages(self):
        doc = ET.parse(self.path)
        root = doc.getroot()

        self.languages = []

        for e in root.findall('language'):
            language = type('', (object,), {'code':e.find('code').text,'description':e.find('description').text})()
            self.languages.append(language)

        return self.languages

    def getLiteral(self,id):
        doc = ET.parse('../language/' + self.module + '_' + self.language + '.xml')
        root = doc.getroot()
        literals = root.find('literals')
        return literals.find(id).text

    def setLast(self, code):  
        doc = ET.parse(self.path)
        root = doc.getroot()

        last = root.find('last')
        last.text = code

        for language in root.findall('language'):           
            description = language.find('description')
            cdata = self.CDATA(description.text)
            # Empty description.text
            description.text=''
            # Add new description.text as CDATA node
            description.append(cdata)

        doc.write(self.path, encoding="utf-8", xml_declaration=True)