from core.Agent import Agent

class Wall(Agent):
    def __init__(self, posX, posY, data=[]):
        # position initiale de la particule
        super(Wall, self).__init__(posX, posY)

    def decide(self, env):
        pass

    def getType(self):
        return 1
    
    def getColor(self):
        return "black"