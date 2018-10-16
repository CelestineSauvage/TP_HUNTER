#coding: utf-8

"""
Contient les caractéristiques des particules et une méthode decide(), destinée à coder le processus de décision de ces particules
"""
class Agent:

    def __init__(self, posX, posY):
        # position initiale de la particule
        self.posX = posX
        self.posY = posY
        self.life = True
        self.time = 0
        self.fearMode = False

    def decide(self, env):
        """
        Méthode qui permet à un agent de décider de son comportement
        """
        raise NotImplementedError( "Should have implemented this" )

    def getType(self):
        """
        """
        raise NotImplementedError( "Should have implemented this" )

    def getColor(self):
        """
        """
        raise NotImplementedError( "Should have implemented this" )

    def dead(self):
        self.life = False
    
    def isAlive(self):
        return self.life
    def on_press(self, key):
        pass