import tkinter as tk
from tkinter import ttk
from Information import Information
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class simulation():
    
    def __init__(self,guiObj):

        self.guiObj = guiObj
        self.workSpace = guiObj.workSpace
        self.modules = guiObj.modules
        self.people = []

    def setup(self,simTime,debug=True):

        self.debug = debug
        self.simTime = simTime
        self.sysTime = 0

        for p in self.people:
            self.workSpace.delete(p.eId)
        self.people = []

        self.modules = self.guiObj.modules
        for m in self.modules:
            self.modules[m].init_run()

    def run(self):

        # record = open("traffic_record","w")

        showPlot = False

        groupInf = {}

        print(self.modules)
        for m in self.modules:
            if self.modules[m].moduleType == "Serv":
                if self.modules[m].isPlot:
                    if not showPlot:
                        informationWin = tk.Toplevel()
                        informationWin.title("Information")
                        showPlot = True
                    
                    group = self.modules[m].group
                    if group not in groupInf:
                        groupInf[group] = Information(informationWin, group)
        
        numGroup = len(groupInf)
        informationWin.geometry("700x"+str(200*numGroup))
        fig = plt.figure()
        canvas = FigureCanvasTkAgg(fig, informationWin)
        canvas.get_tk_widget().place(x=200, y=0, width=500, height= 200*numGroup,anchor=tk.NW)

        ax = fig.add_subplot(1,1,1)
        ax.set_title("Traffic graph", fontsize=12)
        ax.set_xlim((0,300))
        ax.set_xlabel("Time (s)")
        # ax.set_xticklabels([])
        for group in groupInf:
            groupInf[group].line, = ax.step([i for i in range(300)], groupInf[group].plotY, where='post', label=groupInf[group].name)
        ax.legend()
        ax.grid()
        fig.tight_layout()

        def animate(i):
            lines = []
            maxPlot = []
            for group in groupInf:
                maxPlot.append(max(groupInf[group].plotY))
                groupInf[group].line.set_xdata(groupInf[group].plotX)  # update the data
                groupInf[group].line.set_ydata(groupInf[group].plotY)  # update the data
                lines.append(groupInf[group].line)
            ax.set_xlim((groupInf[group].plotX[0],groupInf[group].plotX[-1]+1))
            ax.set_ylim((0, max(maxPlot)+2))
            return lines
        
        ani = animation.FuncAnimation(fig, animate, interval=1000)

        t = 0


        while self.sysTime <= self.simTime and self.guiObj.runSim:
            
            if self.debug:
                print("Systime:",self.sysTime)

            for i,p in enumerate(self.people):
                p.update(self.sysTime)
                if p.state == "onservice":
                    if p.isDraw:
                        self.workSpace.delete(p.eId)
                        p.isDraw = False

            for m in self.modules:
                pout = self.modules[m].update(self.sysTime)

                if pout[0] == 1: 
                    self.people.append(pout[1])
                # elif pout[0] == 2:
                #     rl = ""
                #     for r in pout[1].time:
                #         rl += r[0] + ":" + str(r[1]) + ","
                #     rl += "\n"
                #     record.write(rl)
                #     self.people.remove(pout[1])

                if self.modules[m].moduleType == "Src":
                    if pout[0] == 1: 
                        groupInf[self.modules[m].group].updatePeople()

                if self.modules[m].moduleType == "Sw":
                    if self.modules[m].isPlot:
                        qLen = len(self.modules[m].queue[0])
                        groupInf[self.modules[m].group].updateLen(qLen)

                if self.modules[m].moduleType == "Serv":
                    if self.modules[m].isPlot:
                        qLen = len(self.modules[m].queue[0])
                        groupInf[self.modules[m].group].updateLen(qLen)
                        if pout[0] == 2:
                            if pout[1] != None:
                                qTime = 0
                                servTime = 0
                                for i in range(len(pout[1].time)//2):
                                    qTime += pout[1].time[-2-i*2][1] - pout[1].time[-3-i*2][1] 
                                    servTime += pout[1].time[-1-i*2][1] - pout[1].time[-2-i*2][1] 
                                
                                totalTime = pout[1].time[-1][1] - pout[1].time[0][1] 
                                groupInf[self.modules[m].group].updateTime(qTime, servTime, totalTime)
            
            if t%10 == 0:
                for group in groupInf:
                    groupInf[group].updateGraph()
            t += 1
            
            self.updateGui()

            self.sysTime += 0.1
        
        # record.close()

        self.stop()

    def updateGui(self):

        for m in self.modules:
            self.modules[m].updateGui(self.workSpace)

        for p in self.people:
            if not (p.state == "onservice"):
                p.updateGui(self.workSpace)
        
        self.guiObj.update()

    def stop(self):

        for p in self.people:
            self.workSpace.delete(p.eId)

        for m in self.modules:
            self.modules[m].stop(self.workSpace)
        
        self.people = []

    def plot(self):
        pass