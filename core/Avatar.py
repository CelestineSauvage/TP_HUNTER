from core.Agent import Agent
from getch import KeyListener

"""
"""
class Avatar(Agent):
    def __init__(self, posX, posY, data):
        # position initiale de l'avatar
        super(Avatar, self).__init__(posX, posY)

        self.vector = (0,1)
        self.keyL = KeyListener(self)
        self.keyL.start()
        self.form = "circle"
        self.delay = data[0]

    def decide(self, env):
        """
        Position de l'avatar suivant la dernière saisie clavier du joueur (monde torique)
        """
        self.time += 1

        if self.delay <= self.time:
            self.time = 0
            xp, yp = (self.posX+self.vector[0]+env.l) % env.l, (self.posY+self.vector[1]+env.h) % env.h # met à jour la position

            env.updateValues(self.posX, self.posY)

            case = env.getPositionAgent(xp, yp)

            if (case == None): # regarde si il peut bouger
                env.setAgentPosition(self, xp, yp)
                self.posX, self.posY = xp, yp
                env.updateValues(xp, yp)
                
            elif case.getType() == 3:
                env.kill(xp, yp)

                env.setAgentPosition(self, xp, yp)
                self.posX, self.posY = xp, yp
                env.updateValues(xp, yp)

    def getColor(self):
        """
        """
        return "yellow"

    def on_press(self, key):

        #On change le vector du pac man
        try:
            if key == 0: #down
                self.vector = (0, 1)
            elif key == 1: #up
                self.vector = (0, -1)
            elif key == 2: #left
                self.vector = (-1, 0)
            elif key == 3: #right
                self.vector = (1, 0)
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    def getType(self):
        return 0
