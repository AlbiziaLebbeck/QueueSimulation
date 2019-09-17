import numpy as np
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

        self.arrivrate = 0.005
        self.dstOut = []

        self.servicePerson = None
        
    def init_run(self):
        self.last_arrival_time = np.random.exponential(1/self.arrivrate)

    def update(self,systime):

        if self.last_arrival_time <= systime and len(self.dstOut):

            self.dstOut[0].incoming += 1
            p = People.person(self,self.dstOut[0],self.last_arrival_time)

            interarrtime = np.random.exponential(1/self.arrivrate)

            if interarrtime < 20:
                interarrtime = 20

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
        self.servicePerson = None
        
        self.queue = 0 
            
    def update(self,systime):
        
        if not self.onService and self.queue > 0:
            self.onService = True
            self.queue = 0

            if self.deprate == 0:
                self.depTime = systime
            else:
                self.depTime = systime + np.random.exponential(1/self.deprate)
        
        if self.onService:
            if self.depTime <= systime:
                self.onService = False
                self.incoming -= 1

                p = self.servicePerson
                p.time.append((self.Name + "(out)",self.depTime))

                if len(self.dstOut) > 0:
                    self.servicePerson = None

                    self.dstOut[0].incoming += 1
                    p.target = self.dstOut[0]
                    p.pos = [float(self.pos[0]+20),float(self.pos[1])]
                    p.state = "walking"

                    return [0,None]
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

        self.dstOut = []

    def init_run(self):

        self.onService = False
        self.incoming = 0
        self.servicePerson = None
        
        self.queue = 0 
            
    def update(self,systime):
        
        if not self.onService and self.queue > 0:
            self.onService = True
            self.queue = 0
        
        if self.onService:
            p = self.servicePerson
            if len(self.dstOut) > 0:
                for d in self.dstOut:
                    if d.incoming == 0:
                        p.time.append((self.Name + "(out)",systime))
                        self.onService = False
                        self.incoming -= 1
                        
                        self.servicePerson = None

                        d.incoming += 1
                        p.target = d
                        p.pos = [float(self.pos[0]+20),float(self.pos[1])]
                        p.state = "walking"

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
        self.moduleType = "๋Junc"

        self.num_out = 1
        self.num_in = 99

        self.eId = eId
        self.tEId = 0
        self.pos = pos

        self.dstOut = []

    def init_run(self):

        self.onService = False
        self.incoming = 0
        self.servicePerson = None
        
        self.queue = [0 for i in range(1)]

            
    def update(self,systime):
        
        if not self.onService and self.queue > 0:
            self.onService = True
            self.queue = 0
        
        if self.onService:
            p = self.servicePerson
            if len(self.dstOut) > 0:
                for d in self.dstOut:
                    p.time.append((self.Name + "(out)",systime))
                    self.onService = False
                    self.incoming -= 1
                    
                    self.servicePerson = None

                    d.incoming += 1
                    p.target = d
                    p.pos = [float(self.pos[0]+20),float(self.pos[1])]
                    p.state = "walking"

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