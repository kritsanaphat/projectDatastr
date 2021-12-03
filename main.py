from tkinter import *
import tkinter as tk    
from collections import deque
from tkinter import messagebox



class Stack:
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

class Queue:
    def __init__(self,list = None):
        '''
        if list == None:
            self.item=[]
        else:
            self.item = list
        '''
        self.item = deque()
            
    def enQueue(self,i):
        self.item.append(i)
    
    def deQueue(self):
        #return self.item.pop(0)
        return self.item.popleft()
    
    def isEmpty(self):
        return self.size() == 0

    def size(self):
        return len(self.item)
    
    def __str__(self) :
        s = self.item[0]
        i=1
        if(self.size()>0):
            while(i<self.size()):
                s +=","+" "+self.item[i]
                i+=1
        return s
     
class Sketchpad(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
       
        self.curColor = "black"
        self.color = {0:"black",1:"red",2:"orange",3:"yellow",4:"green",5:"blue",6:"purple"}
        
        #append fuction changcolor
        self.queuefuc_color = Queue()
        self.queuefuc_color.enQueue(self.changeColor0)
        self.queuefuc_color.enQueue(self.changeColor1)
        self.queuefuc_color.enQueue(self.changeColor2)
        self.queuefuc_color.enQueue(self.changeColor3)
        self.queuefuc_color.enQueue(self.changeColor4)
        self.queuefuc_color.enQueue(self.changeColor5)
        self.queuefuc_color.enQueue(self.changeColor6)
        

        #append color
        self.queue_color = Queue()
        for i in range(len(self.color)):
            self.queue_color.enQueue(self.color[i])
        print(self.queue_color)

        self.tool()
        self.thickness = 1
        self.buf = []
        self.stack = Stack()
        self.bind("<Button-1>", self.save_posn) 
        self.bind("<B1-Motion>", self.add_line) 
        self.bind("<ButtonRelease-1>", self.save_progress) 

    def tool(self):
        menubar = Menu(root, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')
        save_ = Menu(menubar,tearoff=0)
        menubar.add_cascade(label='Save', menu= save_)
        save_.add_command(label='Save', command="ff")
        self.tempfuc_color = []
        while self.queuefuc_color.isEmpty() is False:
            self.tempfuc_color.append(self.queuefuc_color.deQueue())
        print(self.tempfuc_color[0])


        self.tempqueue_color = []
        while self.queue_color.isEmpty() is False:
            self.tempqueue_color.append(self.queue_color.deQueue())
        print(self.tempqueue_color[0])
        
        

        color_ = Menu(menubar,tearoff=0)
        color_.add_command(background= self.tempqueue_color[0],command=self.tempfuc_color[0])
        color_.add_command(background= self.tempqueue_color[1],command=self.tempfuc_color[1])
        color_.add_command(background= self.tempqueue_color[2],command=self.tempfuc_color[2])
        # color_.add_command(background= self.tempqueue_color[3],command=self.tempfuc_color[3])
        # color_.add_command(background= self.tempqueue_color[4],command=self.tempfuc_color[4])
        # color_.add_command(background= self.tempqueue_color[5],command=self.tempfuc_color[5])
        # color_.add_command(background= self.tempqueue_color[6],command=self.tempfuc_color[6])
        
        menubar.add_cascade(label='Color',menu = color_)
        root.config(menu = menubar)

        other_ = Menu(color_, tearoff=0)
        other_.add_command(background= self.tempqueue_color[3],command=self.tempfuc_color[3])
        other_.add_command(background= self.tempqueue_color[4],command=self.tempfuc_color[4])
        other_.add_command(background= self.tempqueue_color[5],command=self.tempfuc_color[5])
        other_.add_command(background= self.tempqueue_color[6],command=self.tempfuc_color[6])
        color_.add_cascade(
        label="other",
        menu=other_
                                )

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
            # print(self.stack)

    def openFile(self):
        pass

    def saveFile(self):
        pass

    def changeColor0(self):
        colorChange = "black"
        if self.tempqueue_color[0] != colorChange:
            self.curColor =colorChange
            self.queue_color.enQueue(colorChange)
            self.queuefuc_color.enQueue(self.tempfuc_color[0])
            for i in range(len(self.tempqueue_color)):
                if self.tempqueue_color[i]!=colorChange:
                    self.queue_color.enQueue(self.tempqueue_color[i])
                    self.queuefuc_color.enQueue(self.tempfuc_color[i])
        else:
            for i in range(len(self.tempqueue_color)):
                self.queue_color.enQueue(self.tempqueue_color[i])
                self.queuefuc_color.enQueue(self.tempfuc_color[i])

        self.tool()

    def changeColor1(self):
        colorChange = "red"
        if self.tempqueue_color[0] != colorChange:
            self.curColor =colorChange
            self.queue_color.enQueue(colorChange)
            self.queuefuc_color.enQueue(self.tempfuc_color[1])
            for i in range(len(self.tempqueue_color)):
                if self.tempqueue_color[i]!=colorChange:
                    self.queue_color.enQueue(self.tempqueue_color[i])
                    self.queuefuc_color.enQueue(self.tempfuc_color[i])
        else:
            for i in range(len(self.tempqueue_color)):
                self.queue_color.enQueue(self.tempqueue_color[i])
                self.queuefuc_color.enQueue(self.tempfuc_color[i])
        self.tool()

    def changeColor2(self):
        colorChange = "orange"
        if self.tempqueue_color[0] != colorChange:
            self.curColor =colorChange
            self.queue_color.enQueue(colorChange)
            self.queuefuc_color.enQueue(self.tempfuc_color[2])
            for i in range(len(self.tempqueue_color)):
                if self.tempqueue_color[i]!=colorChange:
                    self.queue_color.enQueue(self.tempqueue_color[i])
                    self.queuefuc_color.enQueue(self.tempfuc_color[i])
        else:
            for i in range(len(self.tempqueue_color)):
                self.queue_color.enQueue(self.tempqueue_color[i])
                self.queuefuc_color.enQueue(self.tempfuc_color[i])
        self.tool()
        
        

    def changeColor3(self):
        colorChange = "yellow"
        if self.tempqueue_color[0] != colorChange:
            self.curColor =colorChange
            self.queue_color.enQueue(colorChange)
            self.queuefuc_color.enQueue(self.tempfuc_color[3])
            for i in range(len(self.tempqueue_color)):
                if self.tempqueue_color[i]!=colorChange:
                    self.queue_color.enQueue(self.tempqueue_color[i])
                    self.queuefuc_color.enQueue(self.tempfuc_color[i])
        else:
            for i in range(len(self.tempqueue_color)):
                self.queue_color.enQueue(self.tempqueue_color[i])
                self.queuefuc_color.enQueue(self.tempfuc_color[i])
        self.tool()

    def changeColor4(self):
        colorChange = "green"
        if self.tempqueue_color[0] != colorChange:
            self.curColor =colorChange
            self.queue_color.enQueue(colorChange)
            self.queuefuc_color.enQueue(self.tempfuc_color[4])
            for i in range(len(self.tempqueue_color)):
                if self.tempqueue_color[i]!=colorChange:
                    self.queue_color.enQueue(self.tempqueue_color[i])
                    self.queuefuc_color.enQueue(self.tempfuc_color[i])
        else:
            for i in range(len(self.tempqueue_color)):
                self.queue_color.enQueue(self.tempqueue_color[i])
                self.queuefuc_color.enQueue(self.tempfuc_color[i])
        self.tool()
        
    def changeColor5(self):
        colorChange = "blue"
        if self.tempqueue_color[0] != colorChange:
            self.curColor =colorChange
            self.queue_color.enQueue(colorChange)
            self.queuefuc_color.enQueue(self.tempfuc_color[5])
            for i in range(len(self.tempqueue_color)):
                if self.tempqueue_color[i]!=colorChange:
                    self.queue_color.enQueue(self.tempqueue_color[i])
                    self.queuefuc_color.enQueue(self.tempfuc_color[i])
        else:
            for i in range(len(self.tempqueue_color)):
                self.queue_color.enQueue(self.tempqueue_color[i])
                self.queuefuc_color.enQueue(self.tempfuc_color[i])
        self.tool()
        

    def changeColor6(self):
        colorChange = "purple"
        if self.tempqueue_color[0] != colorChange:
            self.curColor =colorChange
            self.queue_color.enQueue(colorChange)
            self.queuefuc_color.enQueue(self.tempfuc_color[6])
            for i in range(len(self.tempqueue_color)):
                if self.tempqueue_color[i]!=colorChange:
                    self.queue_color.enQueue(self.tempqueue_color[i])
                    self.queuefuc_color.enQueue(self.tempfuc_color[i])
        else:
            for i in range(len(self.tempqueue_color)):
                self.queue_color.enQueue(self.tempqueue_color[i])
                self.queuefuc_color.enQueue(self.tempfuc_color[i])
        self.tool()
    
    def other(self):
        pass


root = Tk()
sketch = Sketchpad(root)

root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
sketch.bind()
sketch.grid(column=0, row=1, sticky=(N, W, E, S))


root.mainloop()