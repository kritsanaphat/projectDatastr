from tkinter import *
import tkinter as tk    
from collections import deque
import os
from datetime import datetime

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

    def clear(self):
        while self.size() != 0:
            self.pop()

    def __str__(self):
        s = ""
        for i in self.item:
            s += str(i)+' '
        if(s==""):
            return("Empty")
        return s

class Queue:
    def __init__(self):
        self.item = deque()
            
    def enQueue(self,i):
        self.item.append(i)
    
    def deQueue(self):
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

def QuickSort(li, left, right):
    if left + 1 == right:
        if li[left].lower() > li[right].lower():
            li[left], li[right] = li[right], li[left]
        return 
    if left < right:
        pivot = li[left].lower()
        i, j = left+1, right
        while i < j:
            while i < right and li[i].lower() <= pivot:
                i += 1
            while j > left and li[j].lower() >= pivot:
                j -= 1
            if i<j:
                li[i], li[j] = li[j], li[i]
        if j != left:
            li[left], li[j] = li[j], pivot
        QuickSort(li, left, j-1)
        QuickSort(li, j+1, right)

def InsertSort(li):
    for i in range(1, len(li)):
        iEle = li[i]
        for j in range(i, -1, -1):
            if FileData.compare(iEle,li[j-1]) == 0 and j > 0:
                li[j] = li[j-1]
            else:
                li[j] = iEle
                break

class FileData:
    def __init__(self, fileName, dir):
        self.fileName = fileName
        self.dir = dir + "\\" + fileName
        f = open(self.dir, 'r')
        s = f.readline()
        f.close()
        self.time = []
        self.time.append(int(s[:4]))
        self.time.append(int(s[5:7]))
        self.time.append(int(s[8:10]))
        self.time.append(int(s[11:13]))
        self.time.append(int(s[14:16]))
        self.time.append(int(s[17:19]))

    def compare(FD0, FD1):
        for i in range(6):
            if FD0.time[i] > FD1.time[i]:
                return 0
            elif FD0.time[i] < FD1.time[i]:
                return 1

    def compareDate(FD, li):
        for i in range(3):
            if FD.time[i] > li[i]:
                return 0
            elif FD.time[i] < li[i]:
                return 1
            elif i == 2:
                return 2

    def __str__(self):
        return self.fileName + '\n' + self.dir + '\n' + self.time.__str__() + '\n' 

class Sketchpad(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.root = parent
        self.curColor = "black"
        self.color = {0:"black",1:"red",2:"orange",3:"yellow",4:"green",5:"blue",6:"purple",7:"white",8:self['background']}
        self.winState = False
        self.savedir = ""
        self.name = ""
        self.save = True
        self.newState = False

        self.recentColor = Queue()
        self.recentColor.enQueue("black")
        self.recentColor.enQueue("black")
        self.recentColor.enQueue("black")

        self.thickness = 1
        self.thickBG = ['gray', self['background'], self['background'], self['background']]
        self.buf = []
        self.tool()
        self.progress = Stack()
        self.temp = Stack()
        self.bind("<Button-1>", self.save_posn) 
        self.bind("<B1-Motion>", self.add_line) 
        self.bind("<ButtonRelease-1>", self.save_progress)

        try:
            f = open("C:\MyPaint\Configs\Config.txt",'r')
            self.savedir = f.readline()
            f.close()
        except:
            os.chdir("C:\\")
            os.mkdir("MyPaint")
            os.chdir("C:\MyPaint")
            os.mkdir("Configs")
            os.mkdir("Saves")
            f = open("C:\MyPaint\Configs\Config.txt",'w+')
            self.savedir = "C:\MyPaint\Saves"
            f.write(self.savedir)
            f.close()

    def tool(self):
        #main
        menubar = Menu(root, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')
        
        #Menusave
        file_ = Menu(menubar,tearoff=0)
        menubar.add_cascade(label='File', menu= file_)
        file_.add_command(label="New", command=self.newFile)
        file_.add_command(label='Open', command=self.openFile)
        file_.add_command(label='Save', command=self.saveFile)
        file_.add_cascade(label="Change save directory", command=self.chd)
        
        #Menuedit
        edit_ = Menu(menubar,tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_)
        edit_.add_command(label="Undo", command=self.undo)
        edit_.add_command(label="Redo", command=self.redo)
        edit_.add_command(label="Clear", command=self.clearEdit)

        #Menucolor
        color_ = Menu(menubar,tearoff=0)
        menubar.add_cascade(label='Color',menu = color_)
        root.config(menu = menubar)

        recent_ = Menu(color_, tearoff=0)
        color_.add_cascade(label="Recent",menu=recent_)
        
        Rcolor0 = self.recentColor.deQueue()
        Rcolor1 = self.recentColor.deQueue()
        Rcolor2 = self.recentColor.deQueue()
        self.recentColor.enQueue(Rcolor0)
        self.recentColor.enQueue(Rcolor1)
        self.recentColor.enQueue(Rcolor2)

        recent_.add_command(background=Rcolor2,command=self.recentColor2)
        recent_.add_command(background=Rcolor1,command=self.recentColor1)
        recent_.add_command(background=Rcolor0,command=self.recentColor0)

        other_ = Menu(color_, tearoff=0)
        color_.add_cascade(label="General",menu=other_)
        other_.add_command(background= self.color[0],command=self.changeColor0)
        other_.add_command(background= self.color[1],command=self.changeColor1)
        other_.add_command(background= self.color[2],command=self.changeColor2)
        other_.add_command(background= self.color[3],command=self.changeColor3)
        other_.add_command(background= self.color[4],command=self.changeColor4)
        other_.add_command(background= self.color[5],command=self.changeColor5)
        other_.add_command(background= self.color[6],command=self.changeColor6)
        other_.add_command(background= self.color[7],command=self.changeColor7)
        other_.add_command(background= self.color[8],command=self.changeColor8)

        color_.add_command(label="Custom", command=self.customColor)

        #Menuthickness
        size_ = Menu(menubar,tearoff=0)
        menubar.add_cascade(label='Size', menu= size_)
        size_.add_command(label='1px', background=self.thickBG[0], command = self.thickness1)
        size_.add_command(label='3px', background=self.thickBG[1], command = self.thickness3)
        size_.add_command(label='5px', background=self.thickBG[2], command = self.thickness5)
        size_.add_command(label='7px', background=self.thickBG[3], command = self.thickness7)

        #Filename
        if self.name == "":
            self.root.title("MyPaint")
        else:
            self.root.title("MyPaint (" + self.name + ")")
        
        
    def save_posn(self, event):
        self.lastx, self.lasty = event.x, event.y
        if self.winState == True:
            try:
                self.win.attributes()
            except:
                self.winState = False

    def add_line(self, event):
        if self.winState == False:
            if len(self.buf) == 0:
                self.temp.clear()
                self.buf.append(self.curColor)
                self.buf.append(self.thickness)
            self.create_line((self.lastx, self.lasty, event.x, event.y), fill=self.curColor,width=self.thickness)
            self.buf.append(self.lastx)
            self.buf.append(self.lasty)
            self.buf.append(event.x)
            self.buf.append(event.y)
            self.save_posn(event)
            self.save = False
        

    def save_progress(self, event):
        if len(self.buf) != 0:
            self.progress.push(self.buf.copy())
            self.buf.clear()
        if self.winState == True:
            try:
                self.win.attributes()
            except:
                self.winState = False

    def newFile(self):
        def reSave():
            self.winState = False
            self.win.destroy()
            self.newState = True
            self.saveFile()

        def notSave():
            self.winState = False
            self.win.destroy()
            self.save = True
            self.newFile()

        def Close():
            self.winState = False
            self.win.destroy()

        if self.save == True:
            self.clearEdit()
            self.progress.clear()
            self.temp.clear()
            self.buf.clear()
            self.name = ""
            self.save = True
            self.tool()
        else:
            if self.winState == False:
                self.winState = True
                self.win=tk.Toplevel()
                self.win.wm_title("New file")

                l = tk.Label(self.win, text="Do you want to save?",borderwidth=5, height=2)
                l.grid(row=0, column=1, padx=20)
                
                but0 = Button(self.win, text="Yes", command=reSave)
                but0.grid(row=1,column=0,padx=5,pady=10)

                but1 = Button(self.win, text="No", command=notSave)
                but1.grid(row=1,column=1,pady=10)

                but2 = Button(self.win, text="Cancel", command=Close)
                but2.grid(row=1,column=2,padx=5,pady=10)

    def openFile(self):
        def sortName():
            lb.delete(0,END)
            for i in sortByName:
                lb.insert(END, i.fileName + "     (" + str(i.time[0]) + "/" + str(i.time[1]) + '/' + str(i.time[2]) + " at " + str(i.time[3]) + ":" + str(i.time[4]) + ")")

        def sortTime():
            lb.delete(0,END)
            for i in sortByTime:
                lb.insert(END, i.fileName + "     (" + str(i.time[0]) + "/" + str(i.time[1]) + '/' + str(i.time[2]) + " at " + str(i.time[3]) + ":" + str(i.time[4]) + ")")

        def searchByName():
            inp = text0.get("1.0","end-1c")
            if inp == "":
                lb.delete(0,END)
                for i in sortByName:
                    lb.insert(END, i.fileName + "     (" + str(i.time[0]) + "/" + str(i.time[1]) + '/' + str(i.time[2]) + " at " + str(i.time[3]) + ":" + str(i.time[4]) + ")")
            else:
                buf = []
                for i in sortByName:
                    for j in range(len(inp)):
                        if i.fileName[j].lower() != inp[j].lower():
                            break
                        elif j == len(inp) - 1:
                            buf.append(i)
                lb.delete(0,END)
                for i in buf:
                    lb.insert(END, i.fileName + "     (" + str(i.time[0]) + "/" + str(i.time[1]) + '/' + str(i.time[2]) + " at " + str(i.time[3]) + ":" + str(i.time[4]) + ")")

        def searchByTime():
            inp = text1.get("1.0","end-1c")
            if inp == "":
                lb.delete(0,END)
                for i in sortByTime:
                    lb.insert(END, i.fileName + "     (" + str(i.time[0]) + "/" + str(i.time[1]) + '/' + str(i.time[2]) + " at " + str(i.time[3]) + ":" + str(i.time[4]) + ")")
            else :
                if inp[:4].isnumeric() and inp[4] == '/' and inp[5:7].isnumeric() and inp[7] == '/' and inp[8:].isnumeric() and len(inp) == 10:
                    inp = [int(i) for i in inp.split('/')]
                    index = -1
                    left = 0
                    right = len(sortByTime) - 1
                    mid = int((left+right)/2)
                    buf = []
                    while left <= right:
                        if FileData.compareDate(sortByTime[mid], inp) == 2:
                            index = mid
                            break
                        elif FileData.compareDate(sortByTime[mid], inp) == 0:
                            left = mid+1
                        else:
                            right = mid-1
                        mid = int((left+right)/2)
                    if index > -1:
                        while index > 0:
                            if FileData.compareDate(sortByTime[index - 1], inp) == 2:
                                index -= 1
                            else:
                                break
                        while index < len(sortByTime) - 1:
                            buf.append(sortByTime[index])
                            if FileData.compareDate(sortByTime[index + 1], inp) == 2:
                                index += 1
                            else:
                                break
                        lb.delete(0,END)
                        for i in buf:
                            lb.insert(END, i.fileName + "     (" + str(i.time[0]) + "/" + str(i.time[1]) + '/' + str(i.time[2]) + " at " + str(i.time[3]) + ":" + str(i.time[4]) + ")")
                    else :
                        lb.delete(0,END)
                else :
                    lb.delete(0,END)
                    for i in sortByTime:
                        lb.insert(END, i.fileName + "     (" + str(i.time[0]) + "/" + str(i.time[1]) + '/' + str(i.time[2]) + " at " + str(i.time[3]) + ":" + str(i.time[4]) + ")")

        def Open():
            inp = lb.get(ANCHOR)
            if inp != '':
                self.name = inp[0:len(inp)-25]
                direct = self.savedir + "\\" + self.name
                f = open(direct, 'r')
                f.readline()
                progress = f.read()
                #Clear
                self.temp.push("ClearE")
                while self.progress.size() != 0:
                    popData = self.progress.pop()
                    self.temp.push(popData)
                    if popData != "Clear":
                        thck = popData[1]
                        for j in range(2,len(popData),4):
                            lx = popData[j]
                            ly = popData[j+1]
                            evx = popData[j+2]
                            evy = popData[j+3]
                            self.create_line((lx,ly,evx,evy),fill=self["background"],width=thck)
            
                while self.temp.size() != 0:
                    popData = self.temp.pop()
                    if popData == "ClearE":
                        break
                    self.progress.push(popData)
                self.save = True
                self.progress.clear()
                self.buf.clear()
                self.temp.clear()
                buf = []
                st = ""
                statebuf = False
                statest = False
                for i in progress:
                    if i == " ":
                        continue
                    if i == "[":
                        statebuf = True
                    elif i == "]":
                        statebuf = False
                        if st.isnumeric() == True:
                            buf.append(int(st))
                            st = ""
                        self.progress.push(buf.copy())
                        color = buf[0]
                        thck = buf[1]
                        for i in range(2,len(buf),4):
                            lx =  buf[i]
                            ly = buf[i+1]
                            evx = buf[i+2]
                            evy = buf[i+3]
                            self.create_line((lx,ly,evx,evy),fill=color,width=thck)
                        buf.clear()
                    elif i == "'":
                        if statest == False:
                            statest = True
                        else:
                            if statebuf == True:
                                buf.append(st)
                            else:
                                self.clearEdit()
                            st = ""
                            statest = False 
                    elif i == ",":
                        if st.isnumeric() == True:
                            buf.append(int(st))
                            st = ""
                    else:
                        st += i
                self.winState = False
                self.win.destroy()
                self.tool()

        if self.winState == False:
            allFile = os.listdir(self.savedir)
            for i in allFile:
                if i[len(i)-4:len(i)] != ".txt":
                   allFile.remove(i)
            QuickSort(allFile, 0, len(allFile)-1)
            sortByName = []
            for i in allFile:
                sortByName.append(FileData(i,self.savedir))
            sortByTime = sortByName.copy()
            InsertSort(sortByTime)
            
            self.winState = True
            self.win=tk.Toplevel()
            self.win.wm_title("Open")

            l = tk.Label(self.win, text="File name", borderwidth=5, height=2)
            l.grid(row=0, column=0)

            f = Frame(self.win)
            sc = Scrollbar(f,orient=VERTICAL)
            sc1 = Scrollbar(f,orient=HORIZONTAL)
            lb = Listbox(f,width=50,yscrollcommand=sc.set,xscrollcommand=sc1.set)
            sc.config(command=lb.yview)
            sc.pack(side=RIGHT, fill=Y)
            sc1.config(command=lb.xview)
            sc1.pack(side=BOTTOM, fill=X)
            lb.pack(pady=15)
            f.grid(row=1,column=0,padx=25,pady=10)

            f1 = Frame(self.win)
            l = Label(f1, text="Sort by")
            l.grid(row=0,column=0,padx=30,pady=15)
            but0 = Button(f1, text="Name", command=sortName)
            but0.grid(row=1,column=0,pady=15)
            but1 = Button(f1, text="Time", command=sortTime)
            but1.grid(row=2,column=0,pady=15)
            f1.grid(row=1,column=1)

            l = tk.Label(self.win, text="Search by name", borderwidth=5, height=2)
            l.grid(row=2, column=0)

            text0 = Text(self.win, height=1, width=40,)
            text0.grid(row=3,column=0,padx=5,pady=10)

            but2 = Button(self.win, text="Search", command=searchByName)
            but2.grid(row=4,column=0,padx=5,pady=10)

            l = tk.Label(self.win, text="Search by time Year/Month/Date (EX. 2021/12/01)", borderwidth=5, height=2)
            l.grid(row=5, column=0)

            text1 = Text(self.win, height=1, width=40)
            text1.grid(row=6,column=0,padx=5,pady=10)

            but3 = Button(self.win, text="Search", command=searchByTime)
            but3.grid(row=7,column=0,padx=5,pady=10)

            but4 = Button(self.win, text="Open", command=Open)
            but4.grid(row=8,column=0,padx=5,pady=10)

            for i in sortByName:
                lb.insert(END, i.fileName + "     (" + str(i.time[0]) + "/" + str(i.time[1]) + '/' + str(i.time[2]) + " at " + str(i.time[3]) + ":" + str(i.time[4]) + ")")

    def saveFile(self):
        def receiveInput():
            self.name = text.get("1.0","end-1c") + '.txt'
            fname = self.savedir + '\\' + self.name
            f = open(fname, 'w')
            f.writelines(str(datetime.today())+'\n')
            f.writelines(self.progress.__str__())
            self.win.destroy()
            self.winState = False
            self.tool()
            self.save = True
            if self.newState == True:
                self.clearEdit()
                self.progress.clear()
                self.temp.clear()
                self.buf.clear()
                self.name = ""
                self.newState = False
                self.tool()
                
        if self.winState == False and self.name == "":
            self.winState = True
            self.win=tk.Toplevel()
            self.win.wm_title("Save")

            l = tk.Label(self.win, text="Enter file name", borderwidth=5, height=2)
            l.grid(row=0, column=0)

            text = Text(self.win, height=1, width=15,)
            text.grid(row=1,column=0,padx=5)

            but = Button(self.win, text="Okay", command=receiveInput)
            but.grid(row=2,column=0,pady=10)
        
        elif self.winState == False and self.name != "":
            fname = self.savedir + '\\' + self.name
            f = open(fname, 'w')
            f.writelines(str(datetime.today())+'\n')
            f.writelines(self.progress.__str__())
            self.save = True
            if self.newState == True:
                self.clearEdit()
                self.progress.clear()
                self.temp.clear()
                self.buf.clear()
                self.name = ""
                self.newState = False
                self.tool()

    def chd(self):
        def receiveInput():
            self.savedir = text.get("1.0","end-1c")
            f = open("C:\Program Files\MyPaint\Configs\Config.txt",'w+')
            f.write(self.savedir)
            self.win.destroy()
            self.winState = False

        if self.winState == False:
            self.winState = True
            self.win=tk.Toplevel()
            self.win.wm_title("Change save directory")
            
            l = tk.Label(self.win, text="Now : " + self.savedir, borderwidth=5, height=2)
            l.grid(row=0, column=0)

            l2 = tk.Label(self.win, text="New : ", borderwidth=5, height=2)
            l2.grid(row=1, column=0)

            text = Text(self.win, height=1, width=30,)
            text.grid(row=2,column=0,padx=5)

            but = Button(self.win, text="Okay", command=receiveInput)
            but.grid(row=3,column=0,pady=10)

    def undo(self):
        if self.progress.size() > 0 and self.winState == False:
            bufStack = Stack()
            popData = self.progress.pop()
            self.temp.push(popData)
            if popData != "Clear":
                thck = popData[1]
                for j in range(2,len(popData),4):
                    lx = popData[j]
                    ly = popData[j+1]
                    evx = popData[j+2]
                    evy = popData[j+3]
                    self.create_line((lx,ly,evx,evy),fill=self["background"],width=thck)
            #Move to temporary stack
            while self.progress.size() != 0:
                bufStack.push(self.progress.pop())
            #Redraw
            while bufStack.size() != 0:
                redraw = bufStack.pop()
                self.progress.push(redraw)
                if redraw == "Clear":
                    self.clearEdit()
                    self.progress.pop()
                else :
                    color = redraw[0]
                    thck = redraw[1]
                    for i in range(2,len(redraw),4):
                        lx =  redraw[i]
                        ly = redraw[i+1]
                        evx = redraw[i+2]
                        evy = redraw[i+3]
                        self.create_line((lx,ly,evx,evy),fill=color,width=thck)
            self.save = False

    def redo(self):
        if self.temp.size() != 0 and  self.winState == False:
            popData = self.temp.pop()
            if popData == "Clear":
                self.clearEdit()
            else :
                self.progress.push(popData)
                color = popData[0]
                thck = popData[1]
                for j in range(2,len(popData),4):
                    lx = popData[j]
                    ly = popData[j+1]
                    evx = popData[j+2]
                    evy = popData[j+3]
                    self.create_line((lx,ly,evx,evy),fill=color,width=thck)
            self.save = False

    def clearEdit(self):
        if self.winState == False:
            # Erase
            self.temp.push("ClearE")
            while self.progress.size() != 0:
                popData = self.progress.pop()
                self.temp.push(popData)
                if popData != "Clear":
                    thck = popData[1]
                    for j in range(2,len(popData),4):
                        lx = popData[j]
                        ly = popData[j+1]
                        evx = popData[j+2]
                        evy = popData[j+3]
                        self.create_line((lx,ly,evx,evy),fill=self["background"],width=thck)
            
            while self.temp.size() != 0:
                popData = self.temp.pop()
                if popData == "ClearE":
                    break
                self.progress.push(popData)
            self.progress.push("Clear")
            self.save = False

    def recentColor0(self):
        self.curColor = self.recentColor.deQueue()
        self.recentColor.enQueue(self.curColor)

        self.tool()
    
    def recentColor1(self):
        self.recentColor.enQueue(self.recentColor.deQueue())
        self.curColor = self.recentColor.deQueue()
        self.recentColor.enQueue(self.curColor)

        self.tool()

    def recentColor2(self):
        self.recentColor.enQueue(self.recentColor.deQueue())
        self.recentColor.enQueue(self.recentColor.deQueue())
        self.curColor = self.recentColor.deQueue()
        self.recentColor.enQueue(self.curColor)

        self.tool()

    def changeColor0(self):
        self.curColor = self.color[0]
        self.recentColor.deQueue()
        self.recentColor.enQueue(self.curColor)

        self.tool()

    def changeColor1(self):
        self.curColor = self.color[1]
        self.recentColor.deQueue()
        self.recentColor.enQueue(self.curColor)

        self.tool()

    def changeColor2(self):
        self.curColor = self.color[2]
        self.recentColor.deQueue()
        self.recentColor.enQueue(self.curColor)

        self.tool()

    def changeColor3(self):
        self.curColor = self.color[3]
        self.recentColor.deQueue()
        self.recentColor.enQueue(self.curColor)

        self.tool()

    def changeColor4(self):
        self.curColor = self.color[4]
        self.recentColor.deQueue()
        self.recentColor.enQueue(self.curColor)

        self.tool()
        
    def changeColor5(self):
        self.curColor = self.color[5]
        self.recentColor.deQueue()
        self.recentColor.enQueue(self.curColor)

        self.tool()
        
    def changeColor6(self):
        self.curColor = self.color[6]
        self.recentColor.deQueue()
        self.recentColor.enQueue(self.curColor)

        self.tool()

    def changeColor7(self):
        self.curColor = self.color[7]
        self.recentColor.deQueue()
        self.recentColor.enQueue(self.curColor)

        self.tool()

    def changeColor8(self):
        self.curColor = self.color[8]
        print(self.curColor)
        self.recentColor.deQueue()
        self.recentColor.enQueue(self.curColor)

        self.tool()

    def customColor(self):
        def receiveInput():
            chk = "abcdefABCDEF0123456789"
            ch = True
            inp = text.get("1.0","end-1c")
            if len(inp) != 7:
                ch = False
                inp = "       "
            if inp[0] != '#':
                ch = False
            for i in range(1,7):
                if inp[i] not in chk:
                    ch = False
            if ch == True:
                self.win.destroy()
                self.winState = False
                self.curColor = inp
                self.recentColor.deQueue()
                self.recentColor.enQueue(self.curColor)
                
                self.tool()
            else :
                l = tk.Label(self.win, text="Wrong input!", borderwidth=5, height=2)
                l.grid(row=2, column=0)

                but.grid(row=3, column=0)

        if self.winState == False:
            self.winState = True
            self.win=tk.Toplevel()
            self.win.wm_title("Custom Color")

            l = tk.Label(self.win, text="Fill color (Ex. #ffffff)", borderwidth=5, height=2)
            l.grid(row=0, column=0)

            text = Text(self.win, height=1, width=15,)
            text.grid(row=1,column=0,padx=5)

            but = Button(self.win, text="Okay", command=receiveInput)
            but.grid(row=2,column=0,pady=10)

    def thickness1(self):
        self.thickness = 1
        self.thickBG = ['gray', self['background'], self['background'], self['background']]
        self.tool()

    def thickness3(self):
        self.thickness = 3
        self.thickBG = [self['background'], 'gray', self['background'], self['background']]
        self.tool()

    def thickness5(self):
        self.thickness = 5
        self.thickBG = [self['background'], self['background'], 'gray', self['background']]
        self.tool()

    def thickness7(self):
        self.thickness = 7
        self.thickBG = [self['background'], self['background'], self['background'], 'gray']
        self.tool()

    def other(self):
        pass    


root = Tk()
root.title("MyPaint")
sketch = Sketchpad(root)

root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
sketch.bind()
sketch.grid(column=0, row=1, sticky=(N, W, E, S))

root.mainloop()