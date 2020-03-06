import numpy as np
import math
import time
import random

import People

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

        self.arrivrate = 1
        self.seed = Source.Count

        self.servicePerson = None

        self.group = 1
        
    def init_run(self):
        np.random.seed(seed=self.seed)
        self.last_arrival_time = np.random.exponential(1/self.arrivrate*60)

    def update(self,systime):

        if self.last_arrival_time <= systime and len(self.out_port) > 0:

            line = self.out_port[0]
            for i in range(len(line[2].in_port)):
                if line[2].in_port[i] == line:
                    q_id = i
                    break

            p = People.person(self,q_id,self.last_arrival_time)

            np.random.seed(seed=int(systime*10)*self.seed)
            interarrtime = np.random.exponential(1/self.arrivrate*60)

            if interarrtime < 0.4:
                interarrtime = 0.4

            self.last_arrival_time += interarrtime
            
            return [1,p]
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
        self.Name = "Machine" + str(self.Id)
        self.moduleType = "Serv"

        self.num_out = 1
        self.num_in = 1

        self.eId = eId
        self.tEId = 0
        self.pos = pos

        self.deprate = 1.5

        self.group = 1
        self.isPlot = True

    def init_run(self):

        self.onService = False
        self.servicePerson = None
        
        self.queue = [[] for port in self.in_port]
            
    def update(self,systime):
        
        if not self.onService: 
            for i in range(len(self.queue)):
                if len(self.queue[i]) > 0:
                    if self.queue[i][0].state == "wating":
                        self.onService = True
                        self.servicePerson = self.queue[i].pop(0)
                        self.servicePerson.state = "onservice"
                        self.servicePerson.time.append((self.servicePerson.target.Name + "(in)",systime))

                        if self.deprate == 0:
                            self.depTime = systime
                        else:
                            self.depTime = systime + np.random.exponential(1/self.deprate*60)

                        for j in range(len(self.queue[i])):
                            self.queue[i][j].queue = j
        
        if self.onService:
            if self.depTime <= systime:
                self.onService = False

                p = self.servicePerson
                p.time.append((self.Name + "(out)",self.depTime))
                
                if len(self.out_port) > 0:
                    self.servicePerson = None

                    p.target = self.out_port[0][2]
                    p.pos = [float(self.pos[0]+20),float(self.pos[1])]
                    p.state = "walking"

                    line = self.out_port[0]
                    for i in range(len(line[2].in_port)):
                        if line[2].in_port[i] == line:
                            q_id = i
                            break

                    p.queue = len(p.target.queue[q_id])
                    p.target.queue[q_id].append(p)

                    return [0,p]
                else:
                    self.servicePerson = None
                    return [2,p]

        return [0,None]

    def updateGui(self,WS):
        if self.onService:
            WS.itemconfig(self.eId,fill='salmon')
        else:
            WS.itemconfig(self.eId,fill='deepskyblue')
    
    def stop(self,WS):
        WS.itemconfig(self.eId,fill='deepskyblue')

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

        self.isPlot = True

        self.group = 1

    def init_run(self):

        self.onService = False
        self.servicePerson = None
        
        self.queue = [[] for port in self.in_port]
            
    def update(self,systime):
        
        if not self.onService: 
            for i in range(len(self.queue)):
                if len(self.queue[i]) > 0:
                    if self.queue[i][0].state == "wating":
                        self.onService = True
                        self.servicePerson = self.queue[i].pop(0)
                        self.servicePerson.state = "onservice"
                        self.servicePerson.time.append((self.servicePerson.target.Name + "(in)",systime))

                        for j in range(len(self.queue[i])):
                            self.queue[i][j].queue = j
        
        if self.onService:
            if len(self.out_port) > 0:
                for line in self.out_port:
                    for i in range(len(line[2].in_port)):
                        if line[2].in_port[i] == line:
                            q_id = i
                            break

                    incoming = len(line[2].queue[q_id])
                    if line[2].onService:
                        incoming += 1

                    if incoming == 0:
                        p = self.servicePerson
                        p.time.append((self.Name + "(out)",systime))
                        self.onService = False
                        
                        self.servicePerson = None

                        p.target = line[2]
                        p.pos = [float(self.pos[0]+20),float(self.pos[1])]
                        p.state = "walking"

                        p.queue = len(p.target.queue[q_id])
                        p.target.queue[q_id].append(p)

                        return [0,p]
            else:
                self.servicePerson = None
                return [2,p]
            

        return [0,None]

    def updateGui(self,WS):
        if self.onService:
            WS.itemconfig(self.eId,fill='salmon')
        else:
            WS.itemconfig(self.eId,fill='gold')
    
    def stop(self,WS):
        WS.itemconfig(self.eId,fill='gold')

class Junction(Component_Template):

    count = 0

    def __init__(self,eId,pos):
        super().__init__()

        Junction.count += 1

        self.Id = Junction.count
        self.Name = "junction" + str(self.Id)
        self.moduleType = "Junc"

        self.num_out = 1
        self.num_in = 99

        self.eId = eId
        self.tEId = 0
        self.pos = pos

    def init_run(self):

        self.onService = False
        self.servicePerson = None
        
        self.queue = [[] for port in self.in_port]

        x = self.out_port[0][2].pos[0] - 20 - self.pos[0]
        y = self.out_port[0][2].pos[1] - self.pos[1]
        self.max_Qlen = math.sqrt(x**2 + y**2)//20

        self.depTime = 0

            
    def update(self,systime):
        
        if not self.onService:
            for i in range(len(self.queue)):
                if len(self.queue[i]) > 0 and not self.onService:
                    if self.queue[i][0].state == "wating":
                        self.onService = True
                        self.servicePerson = self.queue[i].pop(0)
                        self.servicePerson.state = "onservice"
                        self.servicePerson.time.append((self.servicePerson.target.Name + "(in)",systime))

                        if self.depTime == 0:
                            self.depTime = systime
                        else:
                            self.depTime = systime + 0.4

                        for j in range(len(self.queue[i])):
                            self.queue[i][j].queue = j
        
        if self.onService:
            if len(self.out_port) > 0:
                for i in range(len(self.out_port[0][2].in_port)):
                    if self.out_port[0][2].in_port[i] == self.out_port[0]:
                        q_id = i
                        break

            cur_Qlen = len(self.out_port[0][2].queue[q_id])
            if self.depTime <= systime and cur_Qlen < self.max_Qlen:
                self.onService = False
                
                p = self.servicePerson
                p.time.append((self.Name + "(out)",systime))

                if len(self.out_port) > 0:
                    self.servicePerson = None

                    p.target = self.out_port[0][2]
                    p.pos = [float(self.pos[0]+20),float(self.pos[1])]
                    p.state = "walking"

                    line = self.out_port[0]
                    for i in range(len(line[2].in_port)):
                        if line[2].in_port[i] == line:
                            q_id = i
                            break

                    p.queue = len(p.target.queue[q_id])
                    p.target.queue[q_id].append(p)

                    return [0,p]
                else:
                    self.servicePerson = None
                    return [2,p]
            

        return [0,None]

    def updateGui(self,WS):
        if self.onService:
            WS.itemconfig(self.eId,fill='salmon')
        else:
            WS.itemconfig(self.eId,fill='gold')
    
    def stop(self,WS):
        WS.itemconfig(self.eId,fill='gold')