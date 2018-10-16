from core.Agent import Agent

"""
"""
class Winner(Agent):
    def __init__(self, posX, posY, data=[]):
        # position initiale de l'avatar
        super(Winner, self).__init__(posX, posY)

        self.form = "circle"

    def decide(self, env):
        """
        Position de l'avatar suivant la dernière saisie clavier du joueur (monde torique)
        """
        pass

    def getColor(self):
        """
        """
        return "blue"

    def getType(self):
        return 3

    def dead(self):
        self.life = False
        print("Fini")