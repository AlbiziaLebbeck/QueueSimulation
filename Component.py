import numpy as np
import time
import random

class Component_Template():
    
    def __init__(self):
        self.in_port = []
        self.out_port = []


class Source(Component_Template):
    
    Count = 0

    def __init__(self,eId,pos):
        super().__init__()

        Source.Count += 1
        
        self.Id = Source.Count
        self.Name = "source" + str(self.Id)
        self.moduleType = "Src"

        self.num_out = 1
        self.num_in = 0

        self.eId = eId
        self.tEId = 0
        self.pos = pos

        self.arrivrate = 0.005
        self.dstOut = []
        
    def init_run(self):
        self.last_arrival_time = np.random.exponential(1/self.arrivrate)

    def run(self,systime):

        if self.last_arrival_time <= systime:
            interarrtime = np.random.exponential(1/self.arrivrate)

            if interarrtime < 20:
                interarrtime = 20

            self.last_arrival_time += interarrtime
            
            return [1,self.dstOut[0]]
        else:
            return [0,None]
    
    def updateGui(self,WS):
        pass

    def stop(self,WS):
        pass

class Server(Component_Template):

    count = 0

    def __init__(self,eId,pos):
        super().__init__()

        Server.count += 1

        self.Id = Server.count
        self.Name = "server" + str(self.Id)
        self.moduleType = "Serv"

        self.num_out = 1
        self.num_in = 1

        self.eId = eId
        self.tEId = 0
        self.pos = pos

        self.deprate = 0.005
        self.dstOut = []

    def init_run(self):

        self.onService = False
        self.incoming = 0
        
        self.queue = 0 

        # self.arrCount = 0
        # self.depCount = 0
        # self.arrID = 0
        # self.depID = 0
        # self.servID = 0
        # self.waitingQ = []
        # self.allarriv = []
        # self.allservtime = []
        # self.serverstate = 0
        # self.deptime = (float('Inf'))
        # self.alldep = []
        # self.tstatus = []
        # self.arr_status = []
        # self.dep_status = []

    # def update_output(self,departuretime):
    #     if self.sinkQ != []:
    #         self.sinkQ.allarriv.append(departuretime)
            
    def run(self,systime):
        
        if not self.onService and self.queue > 0:
            self.onService = True
            self.queue = 0

            self.depTime = systime + np.random.exponential(1/self.deprate)
        
        if self.onService:
            if self.depTime <= systime:
                self.onService = False
                self.incoming -= 1

        return [0,None]

    def updateGui(self,WS):
        if self.onService:
            WS.itemconfig(self.eId,fill='salmon')
        else:
            WS.itemconfig(self.eId,fill='deepskyblue')
    
    def stop(self,WS):
        WS.itemconfig(self.eId,fill='deepskyblue')

    def run_old(self,systime):
        #print(self.arrID)
        for server in range(self.num_server):
            if self.deptime[server] <= systime:
                if self.serverstate[server] !=1 :
                    print('error')
                else :
                    self.serverstate[server] = 0
                    self.depCount = self.depCount +1
                    self.update_output(self.deptime[server])
                    # circle = plt.Cirfcircle)
                    self.alldep.append(systime)
                    if len(self.waitingQ) > 0 :
                        self.waitingQ.pop(0)
                        self.serverstate[server] = 1
                        self.deptime[server] = self.deptime[server] +np.random.exponential(1/self.deprate)
                        self.servID = self.servID+1
                        # circle = plt.Circle((systime,50+server*30+3),10,fc='b')
                        # self.ax.add_patch(circle)
                        break
                    else:
                        self.deptime[server] = float('Inf')
                        break

        if len(self.allarriv) > self.arrCount:            
            if self.allarriv[self.arrCount] <= systime:  
                for server in range(self.num_server):
                    if self.serverstate[server]==0:
                        self.serverstate[server]=1
                        self.deptime[server] = self.allarriv[self.arrCount]+np.random.exponential(1/self.deprate)
                        self.servID = self.servID+1
                        # circle = plt.Circle((systime,2+server*1),0.25,fc='y')
                        # self.ax1.add_patch(circle)
                        break
                        
                else :
                    self.waitingQ.append(systime)
                    # circle = plt.Circle((systime,1),0.25,fc='g')
                    # self.ax1.add_patch(circle)
                self.arrCount = self.arrCount+1
        # print(self.allarriv)
        # print(self.deptime[0])
        customer = 0
        for server in range(self.num_server):
            customer = customer + self.serverstate[server]
        
        self.tstatus.append(systime)
        self.arr_status.append(self.arrCount)
        self.dep_status.append(self.depCount)

    def plot(self):
        self.fig = plt.figure(self.ID,figsize=(6,4))
        # self.ax1 = plt.subplot(3,1,1)
        # self.ax2 = plt.subplot(2,1,2)
        # self.ax3 = plt.subplot(2,1,1)
        self.ax3 = plt.subplot(1,1,1)

        # self.ax2.step(self.tstatus,self.arr_status)
        # self.ax2.step(self.tstatus,self.dep_status)
        self.ax3.step(self.tstatus,[self.arr_status[i] - self.dep_status[i] for i in range(len(self.arr_status))])
        print('average',sum([self.arr_status[i] - self.dep_status[i] for i in range(len(self.arr_status))])/1000)

class Switch(Component_Template):

    count = 0

    def __init__(self,eId,pos):
        super().__init__()

        Switch.count += 1

        self.Id = Switch.count
        self.Name = "switch" + str(self.Id)
        self.moduleType = "Sw"

        self.num_out = 99
        self.num_in = 1

        self.eId = eId
        self.tEId = 0
        self.pos = pos

        self.dstOut = []

    def init_run(self):

        self.onService = False
        self.incoming = 0
        
        self.queue = 0 
            
    def run(self,systime):
        
        if not self.onService and self.queue > 0:
            self.onService = True
            self.queue = 0
        
        if self.onService:
            for d in self.dstOut:
                if d.incoming == 0:
                    self.onService = False
                    self.incoming -= 1
                    return [1,d]

        return [0,None]

    def updateGui(self,WS):
        if self.onService:
            WS.itemconfig(self.eId,fill='salmon')
        else:
            WS.itemconfig(self.eId,fill='gold')
    
    def stop(self,WS):
        WS.itemconfig(self.eId,fill='gold')