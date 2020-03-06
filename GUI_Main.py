import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import pickle

import Component
import Simulation
import numpy as np

class guiMain(tk.Frame):
    def __init__(self,root):

        super().__init__(root)

        self.root = root
        self.root.title('Queue Simulation')

        self.winWidth = 1024
        self.winHeight = 768
        self.winSize = str(self.winWidth)+'x'+str(self.winHeight)
        print(self.winWidth)
        print(self.winHeight)

        self.root.geometry(self.winSize)
        print('Main GUI ready....')

        self.Menu = tk.Frame(self.root,borderwidth=2,relief=tk.RIDGE)
        self.Menu.place(x=0,y=0,height=50,width=1023)

        self.btRun = tk.Button(self.Menu,text='Save',command=self.save)
        self.btRun.place(x=0,y=0,height=46,width=49)

        self.btStop = tk.Button(self.Menu,text='Load',command=self.load)
        self.btStop.place(x=50,y=0,height=46,width=49)

        self.btRun = tk.Button(self.Menu,text='Run',command=self.run)
        self.btRun.place(x=120,y=0,height=46,width=49)

        self.btStop = tk.Button(self.Menu,text='Stop',command=self.stop)
        self.btStop.place(x=170,y=0,height=46,width=49)

        self.timeVar = tk.StringVar()
        self.labelTime = tk.Label(self.Menu,text="Simulation time:")
        self.labelTime.place(x=230,y=3,height=40,width=100)
        self.textTime = tk.Entry(self.Menu,bd = 3,textvariable=self.timeVar)
        self.textTime.place(x=330,y=3,height=40,width=50)
        self.labelUnit = tk.Label(self.Menu,text="s")
        self.labelUnit.place(x=380,y=3,height=40,width=20)
        self.timeVar.set("1000")

        # self.btResult = tk.Button(self.Menu,text='Result',command=self.result)
        # self.btResult.place(x=420,y=0,height=46,width=49)

        self.labelMode = tk.Label(self.Menu,text="Mode:")
        self.labelMode.place(x=480,y=3,height=40,width=50)
        self.modeVar = tk.StringVar()
        self.optionMode = tk.OptionMenu(self.Menu, self.modeVar, "Standalone", "Comparison", command=self.setMode)
        self.modeVar.set("Standalone")
        self.optionMode.place(x=530,y=0,height=46,width=110)

        self.runSim = True


        self.moduleMenu = tk.Frame(self.root,borderwidth=2,relief=tk.RIDGE)
        self.moduleMenu.place(x=0,y=50,height=717,width=150)

        self.btSrc = tk.Button(self.moduleMenu,text='Source',command=self.create_src)
        self.btSrc.place(x=0,y=0,height=75,width=146)

        self.btQueue = tk.Button(self.moduleMenu,text='Ticket Machine',command=self.create_server)
        self.btQueue.place(x=0,y=75,height=75,width=146)

        self.btSwitch = tk.Button(self.moduleMenu,text='Switch',command=self.create_switch)
        self.btSwitch.place(x=0,y=150,height=75,width=146)

        self.btJunction = tk.Button(self.moduleMenu,text='Junction',command=self.create_junction)
        self.btJunction.place(x=0,y=225,height=75,width=146)

        self.btLine = tk.Button(self.moduleMenu,text='Link',command=self.create_line)
        self.btLine.place(x=0,y=300,height=75,width=146)

        self.workSpace = tk.Canvas(self.root, width=1023, height=700,background='white')
        self.workSpace.place(x=150,y=50, width=873, height=700)
        self.workSpace.bind("<Button-3>",lambda e: self.rightClick(e))
        self.gridsize = 5
        for col in range(1,1023//(self.gridsize*10)):
            self.workSpace.create_line(col*self.gridsize*10,0,col*self.gridsize*10,717,tags=('grid'),fill='lightgray')
        for row in range(1,717//(self.gridsize*10)):
            self.workSpace.create_line(0,row*self.gridsize*10,1023,row*self.gridsize*10,tags=('grid'),fill='lightgray')

        self.modules = {}
        self.lines = {}

        self.select_object = -1

        self.sim = Simulation.simulation(self)

        self.mode = "Standalone"


##########################################################
#######                  Set Mode                  #######
##########################################################

    def setMode(self, val):
        self.mode = val

        self.modules = {}
        self.lines = {}

        self.workSpace.delete('all')

        for col in range(1,1023//(self.gridsize*10)):
                self.workSpace.create_line(col*self.gridsize*10,0,col*self.gridsize*10,717,tags=('grid'),fill='lightgray')
        for row in range(1,717//(self.gridsize*10)):
            self.workSpace.create_line(0,row*self.gridsize*10,1023,row*self.gridsize*10,tags=('grid'),fill='lightgray')

        if self.mode == "Comparison":
            self.workSpace.create_line(0,7*self.gridsize*10,1023,7*self.gridsize*10,tags=('grid'),fill='gray',width=4,dash=(3,5))


##########################################################
#######                    Save                    #######
##########################################################

    def save(self):
        directory = tk.filedialog.asksaveasfilename(filetypes = (("qsim files","*.qs"),),defaultextension='.qs')
        with open(directory, 'wb') as file_object:
            pickle.dump(self.modules, file_object)
            pickle.dump(self.lines, file_object)

##########################################################
#######                    Load                    #######
##########################################################

    def load(self):
        directory = tk.filedialog.askopenfilename(filetypes = (("qsim files","*.qs"),),defaultextension='.qs')
        with open(directory, 'rb') as file_object:
            modules = pickle.load(file_object)
            lines = pickle.load(file_object)
            self.modules = {}
            self.lines = {}

            module_match = {}

            self.workSpace.delete('all')
            for col in range(1,1023//(self.gridsize*10)):
                self.workSpace.create_line(col*self.gridsize*10,0,col*self.gridsize*10,717,tags=('grid'),fill='lightgray')
            for row in range(1,717//(self.gridsize*10)):
                self.workSpace.create_line(0,row*self.gridsize*10,1023,row*self.gridsize*10,tags=('grid'),fill='lightgray')

            self.mode = "Standalone"
            self.modeVar.set("Standalone")
            for Id in modules:
                x,y = modules[Id].pos

                if modules[Id].moduleType == 'Src':
                    eId = self.workSpace.create_rectangle(x-20,y-20,x+20,y+20,fill='mediumspringgreen',tags=('module','Src'))
                    self.modules[eId] = modules[Id]
                    self.modules[eId].eId = eId

                    if self.modules[eId].group == 2:
                        self.mode = "Comparison"

                elif modules[Id].moduleType == 'Serv':
                    eId = self.workSpace.create_rectangle(x-20,y-20,x+20,y+20,fill='deepskyblue',tags=('module','Serv'))
                    self.modules[eId] = modules[Id]
                    self.modules[eId].eId = eId

                elif modules[Id].moduleType == 'Sw':
                    eId = self.workSpace.create_rectangle(x-20,y-20,x+20,y+20,fill='gold',tags=('module','Sw'))
                    self.modules[eId] = modules[Id]
                    self.modules[eId].eId = eId

                elif modules[Id].moduleType == 'Junc':
                    eId = self.workSpace.create_rectangle(x-20,y-20,x+20,y+20,fill='salmon',tags=('module','Junc'))
                    self.modules[eId] = modules[Id]
                    self.modules[eId].eId = eId
                module_match[Id] = eId
                print(eId,Id)
                self.modules[eId].in_port = []
                self.modules[eId].out_port = []

                if y > 350:
                    self.modules[eId].group = 2
                else:
                    self.modules[eId].group = 1
                
                tEId = self.workSpace.create_text(x,y+30,text=self.modules[eId].Name,anchor=tk.CENTER)
                self.modules[eId].tEId = tEId
            
            if self.mode == "Comparison":
                self.modeVar.set("Comparison")
                self.workSpace.create_line(0,7*self.gridsize*10,1023,7*self.gridsize*10,tags=('grid'),fill='gray',width=4,dash=(3,5))

            
            for line in lines.values():
                src = module_match[line[0]]
                pos_src = self.workSpace.coords(src)
                pos1 = (pos_src[2],(pos_src[1]+pos_src[3])/2)
                dst = module_match[line[1]]
                pos_dst = self.workSpace.coords(dst)
                pos2 = (pos_dst[0],(pos_dst[1]+pos_dst[3])/2)
                lId = self.workSpace.create_line(pos1[0],pos1[1],pos2[0],pos2[1],tags=('Line'),arrow=tk.LAST, width=2)
                self.lines[lId] = [src,dst]

                self.modules[src].out_port.append((lId,self.modules[src],self.modules[dst]))
                self.modules[dst].in_port.append((lId,self.modules[src],self.modules[dst]))

            self.sim = Simulation.simulation(self)

##########################################################
#######            Creat New Component             #######
##########################################################

    def create_src(self):
        self.btSrc.config(relief=tk.SUNKEN)
        self.workSpace.bind("<Button-1>",lambda e: self.add_item(e,'Src'))
    

    def create_server(self):
        self.btQueue.config(relief=tk.SUNKEN)
        self.workSpace.bind("<Button-1>",lambda e: self.add_item(e,'Serv'))


    def create_switch(self):
        self.btSwitch.config(relief=tk.SUNKEN)
        self.workSpace.bind("<Button-1>",lambda e: self.add_item(e,'Sw'))


    def create_junction(self):
        self.btSwitch.config(relief=tk.SUNKEN)
        self.workSpace.bind("<Button-1>",lambda e: self.add_item(e,'Junc'))


    def add_item(self,event,module):
        dg = self.gridsize
        x,y = event.x//dg*dg,event.y//dg*dg

        if module == 'Src':
            eId = self.workSpace.create_rectangle(x-20,y-20,x+20,y+20,fill='mediumspringgreen',tags=('module','Src'))
            self.modules[eId] = Component.Source(eId,[x,y])
            print(eId)

            if self.mode == "Comparison":
                tEId = self.workSpace.create_text(x,y+30,text=self.modules[eId].Name,anchor=tk.CENTER)
                self.modules[eId].tEId = tEId
                seed = eId
                self.modules[eId].seed = seed
                if y <=350:
                    self.modules[eId].group = 1
                    y += 350
                else:
                    self.modules[eId].group = 2
                    y -= 350
                eId = self.workSpace.create_rectangle(x-20,y-20,x+20,y+20,fill='mediumspringgreen',tags=('module','Src'))
                self.modules[eId] = Component.Source(eId,[x,y])
                self.modules[eId].seed = seed
                if y <=350:
                    self.modules[eId].group = 1
                else:
                    self.modules[eId].group = 2
            
            self.btSrc.config(relief=tk.RAISED)


        elif module == 'Serv':
            eId = self.workSpace.create_rectangle(x-20,y-20,x+20,y+20,fill='deepskyblue',tags=('module','Serv'))
            self.modules[eId] = Component.Server(eId,[x,y])
            self.btQueue.config(relief=tk.RAISED)

            if self.mode == "Comparison" and y > 350:
                self.modules[eId].group = 2

        elif module == 'Sw':
            eId = self.workSpace.create_rectangle(x-20,y-20,x+20,y+20,fill='gold',tags=('module','Sw'))
            self.modules[eId] = Component.Switch(eId,[x,y])
            self.btSwitch.config(relief=tk.RAISED)

            if self.mode == "Comparison" and y > 350:
                self.modules[eId].group = 2

        elif module == 'Junc':
            eId = self.workSpace.create_rectangle(x-20,y-20,x+20,y+20,fill='salmon',tags=('module','Junc'))
            self.modules[eId] = Component.Junction(eId,[x,y])
            self.btSwitch.config(relief=tk.RAISED)
        
        tEId = self.workSpace.create_text(x,y+30,text=self.modules[eId].Name,anchor=tk.CENTER)
        self.modules[eId].tEId = tEId

        self.workSpace.unbind("<Button-1>")


##########################################################
#######                 Creat Line                 #######
##########################################################

    def create_line(self):
        self.btLine.config(relief=tk.SUNKEN)
        self.workSpace.bind("<Button-1>",lambda e: self.src_line(e))

    def src_line(self,event):
        x,y = event.x,event.y
        src = [item for item in self.workSpace.find_overlapping(\
            x-20,y-20,x+20,y+20) if 'module' in self.workSpace.gettags(item)]
            
        if len(src) > 0:
            if len(self.modules[src[0]].out_port) < self.modules[src[0]].num_out:
                self.workSpace.itemconfig(src[0],outline='lime')
                pos_src = self.workSpace.coords(src[0])
                pos1 = (pos_src[2],(pos_src[1]+pos_src[3])/2)
                line = self.workSpace.create_line(pos1[0],pos1[1],x,y,tags=('Line'),arrow=tk.LAST, width=2)
                self.workSpace.bind("<Motion>", lambda e: self.moveLink(e,src[0],line))
                self.workSpace.bind("<Button-1>",lambda e: self.end_line(e,src[0],line))
            else:
                print('Link cannot be created')
        else:
            self.btLine.config(relief=tk.RAISED)
            self.workSpace.unbind("<Button-1>")    

    def end_line(self,event,src,line):
        x,y = event.x,event.y
        dst = [item for item in self.workSpace.find_overlapping(\
            x-20,y-20,x+20,y+20) if 'module' in self.workSpace.gettags(item)] #\
                # and 'Src' not in self.workSpace.gettags(item) and item != src]

        if len(dst) > 0:
            if len(self.modules[dst[0]].in_port) < self.modules[dst[0]].num_in:
                pos_src = self.workSpace.coords(src)
                pos1 = (pos_src[2],(pos_src[1]+pos_src[3])/2)
                pos_dst = self.workSpace.coords(dst[0])
                pos2 = (pos_dst[0],(pos_dst[1]+pos_dst[3])/2)
                # line = self.workSpace.create_line(pos1[0],pos1[1],pos2[0],pos2[1],tags=('Line'),arrow=LAST)
                self.workSpace.coords(line,pos1[0],pos1[1],pos2[0],pos2[1])
                self.lines[line] = (src,dst[0])

                self.modules[src].out_port.append((line,self.modules[src],self.modules[dst[0]]))
                self.modules[dst[0]].in_port.append((line,self.modules[src],self.modules[dst[0]]))

                # self.modules[src].dstOut.append([self.modules[dst[0]],len(self.modules[dst[0]].srcIn)])
                # self.modules[dst[0]].srcIn.append([self.modules[src],len(self.modules[src].dstOut)-1])

            else:
                print('Link cannot be created')
                self.workSpace.delete(line)
        else:
            self.workSpace.delete(line)
            
        self.workSpace.unbind("<Motion>")
        self.workSpace.itemconfig(src,outline='black')
        self.btLine.config(relief=tk.RAISED)
        self.workSpace.unbind("<Button-1>")

##########################################################
#######             Right Click Command            #######
##########################################################

    def rightClick(self,event):
        item_list = [item for item in \
                        self.workSpace.find_overlapping(event.x-5, event.y-5, event.x+5, event.y+5) \
                        if not 'grid' in self.workSpace.gettags(item)]
        print(item_list)
        if len(item_list) > 0:
            self.select_object = item_list[0]
            Rpopup = tk.Menu(self.workSpace, tearoff=0)
            if 'module' in self.workSpace.gettags(self.select_object):
                Rpopup.add_command(label="Move",command=self.move_module) # , command=next) etc...
                Rpopup.add_command(label="Delete",command=self.delete_module)
                Rpopup.add_separator()
                Rpopup.add_command(label="Properties",command=self.editPropperties)
            elif 'Line' in self.workSpace.gettags(self.select_object):
                Rpopup.add_command(label="Delete",command=self.delete_module)
            Rpopup.tk_popup(event.x_root, event.y_root)

    
    def move_module(self):
        if 'module' in self.workSpace.gettags(self.select_object):
            self.workSpace.bind("<Motion>", self.moveMotion)
            self.workSpace.bind("<Button-1>",self.moveClick)

    def moveClick(self,event):
        pos = [event.x,event.y]
        self.modules[self.select_object].pos = pos

        self.workSpace.unbind("<Motion>")
        self.workSpace.unbind("<Button-1>")

    def moveMotion(self,event):
        dg = self.gridsize
        px,py = event.x//dg*dg,event.y//dg*dg
        cor = self.workSpace.coords(self.select_object)
        w = cor[2]-cor[0]
        h = cor[3]-cor[1] 
        self.workSpace.coords(self.select_object,px-w/2,py-h/2,px+w/2,py+h/2)
        self.workSpace.coords(self.modules[self.select_object].tEId,px,py+h/2+10)
       
        line = self.modules[self.select_object].out_port
        for l in line:
            lcor = self.workSpace.coords(l[0])
            self.workSpace.coords(l[0],px+w/2,py,lcor[2],lcor[3])
        
        line = self.modules[self.select_object].in_port
        for l in line:
            lcor = self.workSpace.coords(l[0])
            self.workSpace.coords(l[0],lcor[0],lcor[1],px-w/2,py)


    def delete_module(self):
        if 'module' in self.workSpace.gettags(self.select_object):
            line = self.modules[self.select_object].out_port
            for l in line:
                dst = self.lines[l[0]][1]
                for i,j in enumerate(self.modules[dst].in_port):
                    if j[0] == l[0]:
                        self.modules[dst].in_port.pop(i)

                self.workSpace.delete(l[0])
                del self.lines[l[0]]

            line = self.modules[self.select_object].in_port
            for l in line:
                src = self.lines[l[0]][0]
                for i,j in enumerate(self.modules[src].out_port):
                    if j[0] == l[0]:
                        self.modules[src].out_port.pop(i)
                
                self.workSpace.delete(l[0])
                del self.lines[l[0]]

            self.workSpace.delete(self.select_object)
            self.workSpace.delete(self.modules[self.select_object].tEId)
            del self.modules[self.select_object]
            
        elif 'Line' in self.workSpace.gettags(self.select_object):
            src = self.lines[self.select_object][0]
            dst = self.lines[self.select_object][1]

            for i,l in enumerate(self.modules[src].out_port):
                if l[0] == self.select_object:
                    self.modules[src].out_port.pop(i)

            for i,l in enumerate(self.modules[dst].in_port):
                if l[0] == self.select_object:
                    self.modules[dst].in_port.pop(i)
            
            self.workSpace.delete(self.select_object)
            del self.lines[self.select_object]

    def editPropperties(self):
        propWin = tk.Toplevel()
        module = self.modules[self.select_object]
        propWin.title("Properties: " + module.Name)
        # propWin.geometry("500x400")
        # mainFrame = Frame(propWin)
        # mainFrame.pack(side=TOP)
        nameFrame = tk.Frame(propWin, width=300, height=25)
        nameFrame.pack(fill=tk.X)
        nameLabel = tk.Label(nameFrame,text='Name',width=14)
        nameLabel.place(relx=0.02, rely=0.05, relwidth=0.6, relheight= 0.95, anchor=tk.NW)
        nameVar = tk.StringVar()
        nameEntry = tk.Entry(nameFrame,textvariable=nameVar)
        nameVar.set(module.Name)
        nameEntry.place(relx=0.66, rely=0.05, relwidth=0.3, relheight= 0.95, anchor=tk.NW)

        if module.moduleType == 'Src':
            arrFrame = tk.Frame(propWin, width=200, height=25)
            arrFrame.pack(fill=tk.X)

            arrLabel = tk.Label(arrFrame,text='Arrival rate(person/min)',width=14)
            arrLabel.place(relx=0.02, rely=0.05, relwidth=0.6, relheight= 0.95, anchor=tk.NW)
            arrVar = tk.StringVar()
            arrEntry = tk.Entry(arrFrame,textvariable=arrVar)
            arrVar.set(str(module.arrivrate))
            arrEntry.place(relx=0.66, rely=0.05, relwidth=0.3, relheight= 0.95, anchor=tk.NW)
            
            seedFrame = tk.Frame(propWin, width=200, height=25)
            seedFrame.pack(fill=tk.X)
            seedLabel = tk.Label(seedFrame,text='Seed',width=14)
            seedLabel.place(relx=0.02, rely=0.05, relwidth=0.6, relheight= 0.95, anchor=tk.NW)
            seedVar = tk.StringVar()
            seedEntry = tk.Entry(seedFrame,textvariable=seedVar)
            seedVar.set(str(module.seed))
            seedEntry.place(relx=0.66, rely=0.05, relwidth=0.3, relheight= 0.95, anchor=tk.NW)

        elif module.moduleType == 'Serv':

            def setDep(val):
                if val == "custom":
                    depEntry.config(state='normal')
                else:
                    depEntry.config(state='disabled')
                if val == "BTS A":
                    depVar.set("1.28")#0.021
                elif val == "BTS B":
                    depVar.set("1.48")#0.024
                elif val == "MRT":
                    depVar.set("1.32")#0.022
                elif val == "ARL":
                    depVar.set("2.04")

            typeFrame = tk.Frame(propWin, width=200, height=25)
            typeFrame.pack(fill=tk.X)
            typeLabel = tk.Label(typeFrame,text='Type',width=14)
            typeLabel.place(relx=0.02, rely=0.05, relwidth=0.6, relheight= 0.95, anchor=tk.NW)
            typeVar = tk.StringVar()
            typeOption = tk.OptionMenu(typeFrame, typeVar, "custom", "BTS A", "BTS B", "MRT", "ARL", command=setDep)
            typeVar.set("custom")
            typeOption.place(relx=0.56, rely=0.05, relwidth=0.3, relheight= 0.95, anchor=tk.NW)

            depFrame = tk.Frame(propWin, width=200, height=25)
            depFrame.pack(fill=tk.X)
            depLabel = tk.Label(depFrame,text='Service rate(person/min)',width=14)
            depLabel.place(relx=0.02, rely=0.05, relwidth=0.6, relheight= 0.95, anchor=tk.NW)
            depVar = tk.StringVar()
            depEntry = tk.Entry(depFrame,textvariable=depVar)
            depVar.set(str(module.deprate))
            depEntry.place(relx=0.66, rely=0.05, relwidth=0.3, relheight= 0.95, anchor=tk.NW)

            plotFrame = tk.Frame(propWin, width=200, height=25)
            plotFrame.pack(fill=tk.X)
            plotLabel = tk.Label(plotFrame,text='Plot',width=14)
            plotLabel.place(relx=0.02, rely=0.05, relwidth=0.6, relheight= 0.95, anchor=tk.NW)
            plotVar = tk.BooleanVar()
            plotCheck = tk.Checkbutton(plotFrame, variable=plotVar)
            plotCheck.place(relx=0.66, rely=0.05, relwidth=0.3, relheight= 0.95, anchor=tk.NW)
            plotCheck.toggle()
        
        def setProp():
            if module.moduleType == 'Src':
                module.Name = nameVar.get()
                module.arrivrate = float(arrVar.get())
                module.seed = int(seedVar.get())
            elif module.moduleType == 'Serv':
                module.Name = nameVar.get()
                module.deprate = float(depVar.get())
                module.isPlot = plotVar.get()
            self.workSpace.itemconfig(self.modules[self.select_object].tEId,text=nameVar.get())
            propWin.destroy()

        submitFrame = tk.Frame(propWin)
        submitFrame.pack(fill=tk.X)
        CancelButton = tk.Button(submitFrame,text='Cancel',width=6,command=lambda:propWin.destroy())
        CancelButton.pack(side=tk.RIGHT,padx=5,pady=5)
        okButton = tk.Button(submitFrame,text='OK',width=6,command=setProp)
        okButton.pack(side=tk.RIGHT,padx=5,pady=5)
    
    def moveLink(self,event,src,line):
        px,py = event.x,event.y
        pos_src = self.workSpace.coords(src)
        pos1 = (pos_src[2],(pos_src[1]+pos_src[3])/2)
        self.workSpace.coords(line,pos1[0],pos1[1],px,py)
    
##########################################################
#######          Simulation Runing Method          #######
##########################################################

    def stop(self):
        self.runSim = False

    def run(self):

        self.runSim = True

        time = int(self.timeVar.get())
        if time <= 0:
            time = 100000000
        self.sim.setup(time,False)

        for l in self.lines:
            self.workSpace.itemconfigure(l, state = tk.HIDDEN)
        self.sim.run()
        for l in self.lines:
            self.workSpace.itemconfigure(l, state = tk.NORMAL)

        # self.result()


    def result(self):

        result_window = tk.Toplevel()
        result_window.title("Results")

        records = open("traffic_record", "r") 

        in_list = {}
        out_list = {}

        for line in records:
            recs = line.split(",")
            for rec in recs:
                if rec != "\n":
                    module = rec.split(":")[0]
                    if module[-2] == 'n':
                        if module[:-4] not in in_list:
                            in_list[module[:-4]] = tk.IntVar()
                    else:
                        if module[:-5] not in out_list:
                            out_list[module[:-5]] = tk.IntVar()
        
        tk.Label(result_window, text = "start:").grid(row = 0, column = 0, sticky=tk.W)
        tk.Label(result_window, text = "end:").grid(row = 0, column = 1, sticky=tk.W)

        i = 1
        for v in out_list:
            tk.Checkbutton(result_window, text=v, variable = out_list[v]).grid(row=i, column = 0, sticky=tk.W)
            i += 1
        last_row = i

        i = 1
        for v in in_list:
            tk.Checkbutton(result_window, text=v, variable = in_list[v]).grid(row=i, column = 1, sticky=tk.W)
            i += 1

        if i > last_row:
            last_row = i

        def show_result():
            out_l = []
            in_l = []

            print("start from:")
            for v in out_list:
                if out_list[v].get() == 1:
                    out_l.append(v + "(out)")
            print(out_l)
            print("to:")
            for v in in_list:
                if in_list[v].get() == 1:
                    in_l.append(v + "(in)")
            print(in_l)

            queue_time = []
            records = open("traffic_record", "r") 
            for line in records:
                recs = line.split(",")
                start_time = -1
                end_time = -1
                for rec in recs[1:]:
                    if rec != "\n":
                        module = rec.split(":")[0]
                        time = float(rec.split(":")[1])
                        if module in out_l:
                            start_time = time
                        
                        if module in in_l:
                            end_time = time
                        
                        if start_time > 0 and end_time > 0:
                            queue_time.append(end_time - start_time)
                            break
            
            mean = np.mean(queue_time)
            std = np.std(queue_time)
            print(mean,std)

            plt.figure()
            plt.hist(queue_time,20)
            plt.axvline(x=mean, color='#2cf02c')
            plt.axvline(x=mean-std, ls = "--", color='#2ca02c', alpha=0.7)
            plt.axvline(x=mean+std, ls = "--", color='#2ca02c', alpha=0.7)
            plt.ylabel("users",size=12)
            plt.xlabel("waiting time",size=12)
            plt.title('Histogram of Service Time: Average='+("%.2f" % mean)+'s, SD='+("%.2f" % std)+'s')
            plt.pause(1)


        tk.Button(result_window, text="submit",command = show_result).grid(row = last_row,column = 0, columnspan = 2)

            # start_time = float(rec[0].split(":")[1])
            # end_time = float(rec[-2].split(":")[1])
            # wating_time = end_time - start_time

        # print(sum(Q1)/len(Q1),sum(Q2)/len(Q2))
        # print(len(Q1),len(Q2))

        
