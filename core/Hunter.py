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

    def decide(self, env):
        self.current +=1

        if( self.delay == self.current):
            self.current = 0
            nearPos = env.near(self.posX, self.posY)
            
            #Si l'agent peut bouger
            if nearPos:
                newPos , = min(nearPos, key=itemgetter(1))
                env.setAgentPosition(self, newPos[0], newPos[1])

    def getColor(self):
        return "red"