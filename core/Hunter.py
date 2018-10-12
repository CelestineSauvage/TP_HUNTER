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

        if( self.delay == self.current):
            self.current = 0

            nearPos = env.near(self.posX, self.posY) # essaye de chasser la cible
            #Si l'agent peut bouger
            
            if nearPos:
                #On récupère la valeur de la case courant
                minVal = env.getValue(self.posX, self.posY)
                minPos = (self.posX, self.posY)
                #On recherche le min
                for pos, val in nearPos:
                    if val< minVal:
                        minPos = pos
                        minVal = val
                # newPos = min(nearPos, key=itemgetter(1))
                env.setAgentPosition(self, minPos[0], minPos[1])
                self.posX, self.posY = pos

    def getColor(self):
        return "red"
