from core.Agent import Agent

"""
"""
class Defender(Agent):
    def __init__(self, posX, posY, data):
        # position initiale de l'avatar
        super(Defender, self).__init__(posX, posY)

        self.form = "circle"
        self.deadLine = data[0]

    def decide(self, env):
        """
        Position de l'avatar suivant la dernière saisie clavier du joueur (monde torique)
        """
        self.time += 1

        if self.deadLine <= self.time:
            self.dead()

    def getColor(self):
        """
        """
        return "green"

    def getType(self):
        return 3
