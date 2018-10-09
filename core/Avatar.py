from core.agent import Agent

class Fish(Agent):
    def __init__(self, posX, posY, data):
        # position initiale de la particule
        super(Fish, self).__init__(posX, posY)

        # Gestation
        self.gestationDay = data[0]


    def decide(self, env):
        self.gestation+=1
        self.age +=1

        newPos = env.canMove(self.posX, self.posY)

        if (newPos):
            self.updatePosition(env, newPos, Fish, [self.gestationDay])
        return

    def getType(self):
        return 1

    def getColor(self):
        return "green"
