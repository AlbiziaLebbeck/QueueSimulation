import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Information:

    def __init__(self, informationWin, group):

        self.name = "Group "+str(group)

        self.updateLens = 0
        self.updateTimes = 0

        self.queueTime = 0
        self.queueLen = 0
        self.avgQueueLen = 0
        self.servTime = 0
        self.numServ = 0
        self.totalTime = 0

        self.numPeople = 0
        self.numOutPeople = 0

        frame = tk.Frame(informationWin, width=300, height=200)
        xF = tk.Frame(frame, relief=tk.GROOVE, borderwidth=2)
        
        self.queueTimeLabel = tk.Label(xF, text="Average waiting time: "+str(self.queueTime))
        self.avgQueueLabel = tk.Label(xF, text="Average queue length: "+str(self.avgQueueLen))
        self.servTimeLabel = tk.Label(xF, text="Average service time: "+str(self.servTime))
        self.numServLabel = tk.Label(xF, text="Number of service: "+str(self.numServ))
        self.totalTimeLabel = tk.Label(xF, text="Average total time: "+str(self.totalTime))
        # self.numPeopleLabel = tk.Label(xF, text="Number of people: "+str(self.numPeople-self.numOutPeople))

        self.numServLabel.pack(pady=5)
        self.avgQueueLabel.pack(pady=5)
        self.queueTimeLabel.pack(pady=5)
        self.servTimeLabel.pack(pady=5)
        self.totalTimeLabel.pack(pady=5)
        # self.numPeopleLabel.pack(pady=5)


        self.numPlot = 0
        self.plotX = [i for i in range(300)]
        self.plotY = [0 for i in range(300)]
        self.data = []
        
        xF.place(relx=0.01, rely=0.05, relwidth=0.98, relheight= 0.93, anchor=tk.NW)
        tk.Label(frame, text=self.name).place(relx=0.03, rely=0.05,anchor=tk.W)
        frame.place(x=0, y=200*(group-1), width=300, height=200)
    
    def updatePeople(self):
        self.numPeople += 1
        # self.numPeopleLabel.config(text="Number of people: "+str(self.numPeople-self.numOutPeople))
        
    def updateLen(self, qLen, ref=None):

        self.queueLen = qLen
        self.avgQueueLen = (self.avgQueueLen*self.updateLens + self.queueLen)/(self.updateLens+1)

        if ref == None:
            self.avgQueueLabel.config(text="Average queue length: "+str(round(self.avgQueueLen,2))+" person")
        elif ref.avgQueueLen != 0:
            c = "green" if self.avgQueueLen <= ref.avgQueueLen else "red"
            self.avgQueueLabel.config(text="Average queue length: "+str(round(self.avgQueueLen,2))+" person ("+str(round((self.avgQueueLen)/ref.avgQueueLen*100,0))+"%)", fg = c)

        self.updateLens += 1

    def updateTime(self, qTime, servTime, totalTime, ref=None):
        
        self.servTime = (self.servTime*self.numServ + servTime)/(self.numServ+1)
        self.queueTime = (self.queueTime*self.numServ + qTime)/(self.numServ+1)
        self.numServ += 1

        self.totalTime = (self.totalTime*self.numOutPeople + totalTime)/(self.numOutPeople+1)
        self.numOutPeople += 1

        if ref == None:
            self.queueTimeLabel.config(text="Average waiting time: "+str(round(self.queueTime,2))+" s/person")
            self.servTimeLabel.config(text="Average service time: "+str(round(self.servTime,2))+" s/person")
            self.numServLabel.config(text="Number of services: "+str(self.numServ)+" person")
            self.totalTimeLabel.config(text="Average total time: "+str(round(self.totalTime,2))+" s/person")        
            # self.numPeopleLabel.config(text="Number of people: "+str(self.numPeople-self.numOutPeople))
        else:
            c = "green" if self.queueTime <= ref.queueTime else "red"
            if ref.queueTime != 0:
                self.queueTimeLabel.config(text="Average waiting time: "+str(round(self.queueTime,2))+" s/person ("+str(round((self.queueTime)/ref.queueTime*100,0))+"%)", fg=c)
            c = "green" if self.servTime <= ref.servTime else "red"
            if ref.servTime != 0:
                self.servTimeLabel.config(text="Average service time: "+str(round(self.servTime,2))+" s/person ("+str(round((self.servTime)/ref.servTime*100,0))+"%)", fg=c)
            c = "green" if self.numServ >= ref.numServ else "red"
            if ref.numServ != 0:
                self.numServLabel.config(text="Number of services: "+str(self.numServ)+" person ("+str(round((self.numServ)/ref.numServ*100,0))+"%)", fg=c)
            c = "green" if self.totalTime <= ref.totalTime else "red"
            if ref.totalTime != 0:
                self.totalTimeLabel.config(text="Average total time: "+str(round(self.totalTime,2))+" s/person ("+str(round((self.totalTime)/ref.totalTime*100,0))+"%)", fg=c)      

        self.updateTimes += 1


    def updateGraph(self):

        if self.numPlot < len(self.plotY):
            self.plotY[self.numPlot] = self.numPeople-self.numOutPeople
        else:
            self.plotX.pop(0)
            self.plotX.append(self.plotX[-1]+1)
            self.plotY.pop(0)
            self.plotY.append(self.numPeople-self.numOutPeople)

        self.data.append(self.numPeople-self.numOutPeople)
        self.numPlot += 1