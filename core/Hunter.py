import sys
from core.Agent import Agent
from operator import itemgetter


"""

"""
class Hunter(Agent):
    def __init__(self, posX, posY, data):
        # position initiale de la particule
        super(Hunter, self).__init__(posX, posY)

        # Gestation
        self.delay = data[0]
        self.form = "circle"
        self.fearMode = False
        self.nfear = 0
        self.maxfear = 5

    def decide(self, env):
        #notion de délai pour les hunters
        self.time +=1
        

        if self.delay <= self.time :
            self.time = 0

            nearPos = env.near(self.posX, self.posY) # essaye de chasser la cible
            #Si l'agent peut bouger
            if nearPos:
                
                #nearPos += [(None, env.getValue(self.posX, self.posY))
                if not self.fearMode:
                    self.nfear = 0
                    newPos = min(nearPos, key=itemgetter(2))
                else:
                    self.nfear += 1
                    if self.nfear >= self.maxfear:
                        self.fearMode = False
                    newPos = max(nearPos, key=itemgetter(2))

                if (newPos[1] != None and newPos[1].getType() == 0):
                    env.kill(newPos[0][0], newPos[0][1])
                    env.setAgentPosition(self, newPos[0][0], newPos[0][1])
                    self.posX, self.posY = newPos[0]
                else:
                    while len(nearPos) != 0:
                        #On regarde si c'est un mur
                        if(newPos[1] != None):
                            nearPos.remove(newPos)
                            newPos = min(nearPos, key=itemgetter(2))
                        else:
                            env.setAgentPosition(self, newPos[0][0], newPos[0][1])
                            self.posX, self.posY = newPos[0]
                            return

    def getColor(self):
        return "red"

    def getType(self):
        return 2
