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
        self.current = 0
        self.form = "circle"

    def decide(self, env):
        #notion de délai pour les hunters
        self.current +=1


        if self.delay <= self.current :
            self.current = 0

            nearPos = env.near(self.posX, self.posY) # essaye de chasser la cible
            #Si l'agent peut bouger
            if nearPos:
                #nearPos += [(None, env.getValue(self.posX, self.posY))]
                newPos = min(nearPos, key=itemgetter(2))

                if (newPos[1] != None and newPos[1].getType() == 0):
                    env.kill(newPos[0][0], newPos[0][1])
                    env.setAgentPosition(self, newPos[0][0], newPos[0][1])
                    self.posX, self.posY = newPos[0]
                else:
                    while True:
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
