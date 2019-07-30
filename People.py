import math

class person():

    def __init__(self,src,target,timeCreate):

        self.dz = 1
        self.size = 20

        self.target = target
        self.pos = [float(src.pos[0]+20),float(src.pos[1])]

        x = int(self.pos[0])
        y = int(self.pos[1])

        self.state = "walking"

        self.time = [(src.Name + "(in)",timeCreate)]

        self.isDraw = False

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

        
        if not self.isDraw:
            self.isDraw = True
            self.eId = WS.create_oval(x-self.size//2,y-self.size//2,x+self.size//2,y+self.size//2,fill='salmon')
        else:
            WS.coords(self.eId,x-self.size//2,y-self.size//2,x+self.size//2,y+self.size//2)

