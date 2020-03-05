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

        frame = tk.Frame(informationWin, width=200, height=200)
        xF = tk.Frame(frame, relief=tk.GROOVE, borderwidth=2)
        
        self.queueTimeLabel = tk.Label(xF, text="Queue time: "+str(self.queueTime))
        self.avgQueueLabel = tk.Label(xF, text="Queue length: "+str(self.avgQueueLen))
        self.servTimeLabel = tk.Label(xF, text="Service time: "+str(self.servTime))
        self.numServLabel = tk.Label(xF, text="Number of service: "+str(self.numServ))
        self.totalTimeLabel = tk.Label(xF, text="Total time: "+str(self.totalTime))
        # self.numPeopleLabel = tk.Label(xF, text="Number of people: "+str(self.numPeople-self.numOutPeople))

        self.queueTimeLabel.pack(pady=5)
        self.avgQueueLabel.pack(pady=5)
        self.servTimeLabel.pack(pady=5)
        self.numServLabel.pack(pady=5)
        self.totalTimeLabel.pack(pady=5)
        # self.numPeopleLabel.pack(pady=5)


        self.numPlot = 0
        self.plotX = [i for i in range(300)]
        self.plotY = [0 for i in range(300)]
        
        xF.place(relx=0.01, rely=0.05, relwidth=0.98, relheight= 0.93, anchor=tk.NW)
        tk.Label(frame, text=self.name).place(relx=0.03, rely=0.05,anchor=tk.W)
        frame.place(x=0, y=200*(group-1), width=200, height=200)
    
    def updatePeople(self):
        self.numPeople += 1
        # self.numPeopleLabel.config(text="Number of people: "+str(self.numPeople-self.numOutPeople))
        
    def updateLen(self, qLen):

        self.queueLen = qLen
        self.avgQueueLen = (self.avgQueueLen*self.updateLens + self.queueLen)/(self.updateLens+1)

        self.avgQueueLabel.config(text="Queue length: "+str(round(self.avgQueueLen,2)))

        self.updateLens += 1

    def updateTime(self, qTime, servTime, totalTime):
        
        self.servTime = (self.servTime*self.numServ + servTime)/(self.numServ+1)
        self.queueTime = (self.queueTime*self.numServ + qTime)/(self.numServ+1)
        self.numServ += 1

        self.queueTimeLabel.config(text="Queue time: "+str(round(self.queueTime,2)))
        self.servTimeLabel.config(text="Service time: "+str(round(self.servTime,2)))
        self.numServLabel.config(text="Service number: "+str(self.numServ))

        self.updateTimes += 1

        self.totalTime = (self.totalTime*self.numOutPeople + totalTime)/(self.numOutPeople+1)
        self.numOutPeople += 1

        self.totalTimeLabel.config(text="Total time: "+str(round(self.totalTime,2)))        
        # self.numPeopleLabel.config(text="Number of people: "+str(self.numPeople-self.numOutPeople))


    def updateGraph(self):

        if self.numPlot < len(self.plotY):
            self.plotY[self.numPlot] = self.numPeople-self.numOutPeople
        else:
            self.plotX.pop(0)
            self.plotX.append(self.plotX[-1]+1)
            self.plotY.pop(0)
            self.plotY.append(self.numPeople-self.numOutPeople)
        self.numPlot += 1