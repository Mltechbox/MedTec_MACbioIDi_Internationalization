'''
Created on 26 may. 2017

@author: marilola.afonso@gmail.com
'''

import tkinter
from tkinter import ttk
from tkinter import messagebox
import xml.etree.ElementTree as ET
from root.nested.language import mdasLiteral

class simpleapp_tk(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.geometry("600x300")

        # Get Languages
        self.literal = mdasLiteral('module1')
        self.langCode = []
        self.langDescription = []
        for e in self.literal.getLanguages():
            self.langCode.append(e.code) 
            self.langDescription.append(e.description)

        self.comboBox = ttk.Combobox(self)
        self.comboBox.place(x=450,y=10)
        self.comboBox.state(['readonly'])
        self.comboBox['values'] = self.langDescription
        self.comboBox.bind("<<ComboboxSelected>>", self.OnOptionSelect)

        code = self.literal.getLanguage(self.literal)
        i = self.langCode.index(code)
        self.comboBox.current(i)
        #

        self.entryText =  tkinter.StringVar()
        self.entry = tkinter.Entry(self,textvariable=self.entryText)
        self.entry.id = 'l_00001'
        self.entry.place(x=100,y=60)
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryText.set(mdasLiteral('module1').getLiteral('l_00001'))

        self.labelText = tkinter.StringVar()
        self.label = tkinter.Label(self,textvariable=self.labelText,anchor="w")
        self.label.id = 'l_00002'
        self.label.place(x=10,y=60)
        self.labelText.set(self.literal.getLiteral('l_00002'))


        self.button = tkinter.Button(self,text=self.literal.getLiteral('l_00003'),command=self.OnButtonClick)
        self.button.id = 'l_00003'
        self.button.place(x=500,y=250)

    def OnButtonClick(self):
        print ("You clicked the button !")

    def OnPressEnter(self,event):
        print ("You pressed enter !")
        self.labelText.set(self.entryText.get() + " You pressed enter !")

    def OnOptionSelect(self,event):
        print ("Option selected !")
        i = self.comboBox.current()
        print (i)
        language = self.langCode[i]
        print (language)

        doc = ET.parse('../language/module1_' + language + '.xml')
        root = doc.getroot()
        literals = root.find('literals')

        literal = literals.find(self.label.id).text
        print(literal)
        self.labelText.set(literal)

        literal = literals.find(self.button.id).text
        print(literal)
        self.button['text'] = literal

        literal = literals.find(self.entry.id).text
        print(literal)
        self.entryText.set(literal)

        self.literal.setLast(language)
        
        messagebox.showinfo("mdasMessage", "Changes will take effect at the next reload") 

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('mdasLiteral')
    app.mainloop()