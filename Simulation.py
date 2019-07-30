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

        record = open("traffic_record","w")
        
        while self.sysTime <= self.simTime and self.guiObj.runSim:
            
            if self.debug:
                print("Systime:",self.sysTime)

            for i,p in enumerate(self.people):
                p.update(self.sysTime)
                if p.state == "onservice":
                    if p.isDraw:
                        self.workSpace.delete(p.eId)
                        p.isDraw = False
                        p.time.append((p.target.Name + "(in)",self.sysTime))
                        p.target.servicePerson = p

            for m in self.modules:
                pout = self.modules[m].update(self.sysTime)

                if pout[0] == 1: 
                    self.people.append(pout[1])
                elif pout[0] == 2:
                    rl = ""
                    for r in pout[1].time:
                        rl += r[0] + ":" + str(r[1]) + ","
                    rl += "\n"
                    record.write(rl)
                    self.people.remove(pout[1])
            
            self.updateGui()

            self.sysTime += 1
        
        record.close()

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