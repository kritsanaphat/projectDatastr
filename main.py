from tkinter import *
import tkinter as tk

class Stack():
    def __init__(self,list = None):
        if list == None:
            self.item = []
        else:
            self.item=list

    def push(self,i):
        self.item.append(i)

    def pop(self):
        return self.item.pop()

    def size(self):
         return len(self.item) 

    def __str__(self):
        s = ""
        for i in self.item:
            s += str(i)+' '
        if(s==""):
            return("Empty")
        return s

class Queue():
    passlm;ml[]
class Sketchpad(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.curColor = "black"
        self.color = {0:"black",1:"red",2:"orange",3:"yellow",4:"green",5:"blue",6:"purple",7:self['background']}
        self.thickness = 1
        self.buf = []
        self.stack = Stack()
        self.bind("<Button-1>", self.save_posn) 
        self.bind("<B1-Motion>", self.add_line) 
        self.bind("<ButtonRelease-1>", self.save_progress) 
        
    def save_posn(self, event):
        self.lastx, self.lasty = event.x, event.y

    def add_line(self, event):
        if len(self.buf) == 0:
            self.buf.append(self.curColor)
            self.buf.append(self.thickness)
        self.create_line((self.lastx, self.lasty, event.x, event.y), fill=self.curColor,width=self.thickness)
        self.buf.append(self.lastx)
        self.buf.append(self.lasty)
        self.buf.append(event.x)
        self.buf.append(event.y)
        self.save_posn(event)

    def save_progress(self, event):
        if len(self.buf) != 0:
            self.stack.push(self.buf.copy())
            self.buf.clear()
            print(self.stack)

    def openFile(self):
        pass

    def saveFile(self):
        pass

    def changeColor0(self):
        self.curColor = self.color[0]

    def changeColor1(self):
        self.curColor = self.color[1]

    def changeColor2(self):
        self.curColor = self.color[2]

    def changeColor3(self):
        self.curColor = self.color[3]

    def changeColor4(self):
        self.curColor = self.color[4]

    def changeColor5(self):
        self.curColor = self.color[5]

    def changeColor6(self):
        self.curColor = self.color[6]

    def changeColor7(self):
        self.curColor = self.color[7]
    
    def ChangeThickness0(self):
        self.thicknes = 1
    
    def ChangeThickness1(self):
        self.thicknes = 3

    def ChangeThickness2(self):
        self.thicknes = 5
        

root = Tk()
menubar = Menu(root)

save_ = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Save', menu= save_)
save_.add_command(label='Save', command=None)


color = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Color',menu = color)
color.add_command(background='red',command=None)

root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
sketch = Sketchpad(root)
sketch.bind()
sketch.grid(column=0, row=1, sticky=(N, W, E, S))

root.config(menu = menubar)
mainloop()