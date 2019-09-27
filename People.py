import math

class person():

    def __init__(self,src,q_id,timeCreate):

        self.dz = 5
        self.size = 20

        self.target = src.out_port[0][2]
        self.q_id = q_id
        
        self.queue = len(self.target.queue[q_id])
        self.target.queue[q_id].append(self)

        self.pos = [float(src.pos[0]+20),float(src.pos[1])]

        x = self.target.pos[0] - 20 - self.pos[0]
        y = self.target.pos[1] - self.pos[1]
        self.max_z = math.sqrt(x**2 + y**2)

        self.state = "walking"

        self.time = [(src.Name + "(out)",timeCreate)]

        self.isDraw = False

    def update(self,system):

        if not (self.state == "onservice"): 

            X = self.target.pos[0] - 20 - self.pos[0]
            Y = self.target.pos[1] - self.pos[1]
            Z = math.sqrt(X**2 + Y**2)

            if Z > self.size/2 + self.queue*self.size:

                self.state = "walking"

                dx = self.dz*X/Z
                dy = self.dz*Y/Z

                self.pos[0] += dx
                self.pos[1] += dy
            
            else:
                self.state = "wating"


    def updateGui(self,WS):

        x = int(self.pos[0])
        y = int(self.pos[1])

        
        if not self.isDraw:
            self.isDraw = True
            self.eId = WS.create_oval(x-self.size//2,y-self.size//2,x+self.size//2,y+self.size//2,fill='salmon')
        else:
            WS.coords(self.eId,x-self.size//2,y-self.size//2,x+self.size//2,y+self.size//2)

