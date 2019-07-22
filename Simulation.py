import math

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

        for m in self.modules:
            self.modules[m].init_run()

    def run(self):
        
        while self.sysTime <= self.simTime:
            
            if self.debug:
                print("Systime:",self.sysTime)

            for p in self.people:
                p.update(self.sysTime)
                if p.state == "onservice":
                    self.workSpace.delete(p.eId)

            for m in self.modules:
                pout = self.modules[m].run(self.sysTime)

                for i in range(pout[0]): 
                    target = pout[1]
                    target.incoming += 1
                    self.people.append(person(self.modules[m],target,self.workSpace))
            
            self.updateGui()

            self.sysTime += 1
        
        self.stop()

    def updateGui(self):

        for m in self.modules:
            self.modules[m].updateGui(self.workSpace)

        for p in self.people:
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


class person():

    def __init__(self,src,target,WS):

        self.dz = 1
        self.size = 20

        self.target = target
        self.pos = [float(src.pos[0]+20),float(src.pos[1])]

        x = int(self.pos[0])
        y = int(self.pos[1])
        self.eId = WS.create_oval(x-self.size//2,y-self.size//2,x+self.size//2,y+self.size//2,fill='salmon')

        self.state = "walking"

    def update(self,system):

        if not (self.state == "onservice"): 

            X = self.target.pos[0]-20 - self.pos[0]
            Y = self.target.pos[1] - self.pos[1]
            Z = math.sqrt(X**2 + Y**2)

            if Z > self.size/2 + self.target.queue*self.size:

                self.state = "walking"

                dx = self.dz*X/Z
                dy = self.dz*Y/Z

                self.pos[0] += dx
                self.pos[1] += dy
            
            elif self.state == "walking":
                self.state = "wating"
                self.target.queue += 1

            if Z <= self.size/2 and (not self.target.onService):
                self.state = "onservice"

    def updateGui(self,WS):
        x = int(self.pos[0])
        y = int(self.pos[1])
        WS.coords(self.eId,x-self.size//2,y-self.size//2,x+self.size//2,y+self.size//2)

