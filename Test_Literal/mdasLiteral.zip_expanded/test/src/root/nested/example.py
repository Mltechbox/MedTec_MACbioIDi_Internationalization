'''
Created on 26 may. 2017

@author: marilola.afonso@ulpgc.com
@organization: MACbioIDi
@version: 0.0 for NAMIC 25th Project Week. Summer 2017
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
        if self.literal.getLanguage(self.literal) == 'ar':
            print ("Combo Ok")
            self.comboBox.place(x=10,y=10)
        else:
            self.comboBox.place(x=450,y=10)
        self.comboBox.state(['readonly'])
        self.comboBox['values'] = self.langDescription
        self.comboBox.bind("<<ComboboxSelected>>", self.OnOptionSelect)

        code = self.literal.getLanguage(self.literal)
        i = self.langCode.index(code)
        self.comboBox.current(i)
        #

        self.entryText =  tkinter.StringVar()
        self.entry = tkinter.Entry(self,textvariable=self.entryText, justify='left')
        if self.langCode[i] == 'ar':
            print ("Estamos en arabe")
            self.entry.place(x=400,y=60)
            self.entry = tkinter.Entry(self,textvariable=self.entryText,justify='right')
        else:
            self.entry.place(x=100,y=60)
            self.entry = tkinter.Entry(self,textvariable=self.entryText, justify='left')

        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryText.set(self.literal.getLiteral('l_00001'))

        self.labelText = tkinter.StringVar()
        self.label = tkinter.Label(self,textvariable=self.labelText,anchor="w")
        if self.langCode[i] == 'ar':
            self.label.place(x=550,y=60)
        else:
            self.label.place(x=10,y=60)

        self.labelText.set(self.literal.getLiteral('l_00002'))

        self.button = tkinter.Button(self,text=self.literal.getLiteral('l_00003'),command=self.OnButtonClick)
        if self.langCode[i] == 'ar':
            self.button.place(x=100,y=250)
        else:
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
        ''' Combo box '''
        if language == 'ar':
            self.comboBox.place(x=10,y=10)
            self.comboBox.align="right"
        else:
            self.comboBox.place(x=450,y=10)
        ''' Text box '''    
        if language == 'ar':
            print ("Estamos en arabe")
            self.entry.place(x=400,y=60)
            self.entry = tkinter.Entry(self,textvariable=self.entryText,justify='right')
        else:
            self.entry.place(x=100,y=60)
            self.entry = tkinter.Entry(self,textvariable=self.entryText, justify='left')

        ''' Label '''    
        if language == 'ar':
            self.label.place(x=550,y=60)
        else:
            self.label.place(x=10,y=60)
        ''' Button '''        
        if language == 'ar':
            self.button.place(x=100,y=250)
        else:
            self.button.place(x=500,y=250)    
        

        doc = ET.parse('../language/module1_' + language + '.xml')
        root = doc.getroot()
        literals = root.find('literals')

        literal = literals.find('l_00001').text
        print(literal)
        self.labelText.set(literal)

        literal = literals.find('l_00003').text
        print(literal)
        self.button['text'] = literal

        literal = literals.find('l_00002').text
        print(literal)
        self.entryText.set(literal)

        self.literal.setLast(language)
        
        messagebox.showinfo("mdasMessage", "Changes will take effect at the next reload") 

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('mdasLiteral')
    app.mainloop()