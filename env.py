#coding: utf-8
from core import *
import random
import numpy as np

# LISTE INITIALISEE UNE FOIS POUR LES POSTIONS ET LES POISSONS


"""
Environnement sous forme de grille 2D (coordonnées entières et environnement discret) où sont placés les particules.
Celui-ci peut-être torique ou non
"""

class Env:
    def __init__(self, l, h, size):
        self.l = l
        self.h = h
        self.grid = []
        self.l_agents =[]
        self.size = size

        self.vector = [(0,-1), (1,0), (0,1), (-1,0)]

        #Initialisation de la grille
        self.grid = [[(None, -1)] * (self.h) for _ in range(self.l)]

    #############################################
    #   Opération primitive sur l'environement  #
    #############################################

    def getPosition(self, posX, posY):
        """
        Retourne ce qu'il y a à la position x,y
        """
        return self.grid[posX][posY]

    def setPosition(self, agent, posX, posY):
        """
        Set un agent à la position x, y sur la grille
        """
        self.grid[posX][posY]=(agent, self.getPosition(posX,posY)[1])

    def setValue(self, posX, posY, value):
        """
        """
        self.grid[posX][posY] = (self.grid[posX][posY], value)

    def unsetAgent(self, posX, posY):
        """
        Supprime l'agent de la grille qui se trouve à la position posX, posY
        """
        self.setPosition(None, posX, posY)

    ##########################################
    #   Opération primitive sur les agents  #
    #########################################

    def generate(self, n, classAgent, data=[]):
        """
        Place n agent(s) aléatoirement sur la grille
        """
        i = 0

        while (i < n) : # on génère les n agents dans le tableau

            # pour chaque agent, on le place aléatoirement sur la map
            posX = random.randint(0, self.l-1)
            posY = random.randint(0, self.h-1)
            if (self.getPosition(posX, posY)[0] == None): # si pas d'agent
                agent = classAgent(posX, posY, data)
                self.setAgentPosition(agent, posX, posY)
                self.l_agents.append(agent)
                i += 1

    def setAgentPosition(self, agent, posX, posY):
        """
        Set un agent à la position x, y sur la grille
        """
        if (self.getPosition(posX, posY))[0] == None:
            self.unsetAgent(agent.posX, agent.posY)

            self.setPosition(agent, posX, posY)

    def resetValue(self):
        """
        Set toutes les valeurs de la grille à -1
        """
        for width in self.grid:
            for pos in width:
                pos = (pos[0], -1)

    def updateValues(self, x, y):
        """
        Par rapport à des coordonnées, déploie l'algorithme de Algo de Dijkstra, càd donne une valeur à chaque case de la grille suivant sa proximité avec la cible en posX,posY
        """
        self.resetValue() #reset des valeurs
        fil = list() # file pour les cases
        count  = 0 # valeur à mettre sur la case

        for vector in self.vector:
            xp, yp = (x+vector[0]+self.l) % self.l, (y+vector[1]+self.h) % self.h
            fil.append((xp, yp))

        while fil : # tant qu'il y a des cases à compléter
            #Compteur du parcours
            count +=1
            #Prochaine position à mettre à jour
            newFil = list()

            print("coucou")
            #On parcours les positions à mettre à jour
            for case in fil:
                if(case[1] == -1 and case[0] == None):
                    self.setValue(case[0][0], case[0][1], count)

                    #On définit les voisins
                    # newFil += self.near(case[0][0], case[0][1])
                    for vector in self.vector:
                        xp, yp = (case[0][0]+vector[0]+self.l) % self.l, (case[0][1]+vector[1]+self.h) % self.h
                        newFil.append((xp, yp))

            fil = newFil
        # self.printGrid()
        return

    def near(self, x, y):
        """
        Regarde les case autour de l'agent et prend une case disponible
        """
        self.cptPos = 0
        res =[]
        #On parcours toutes les case adjacent
        for dx, dy in self.vector:
            xp, yp = (x+dx+self.l) % self.l, (y+dy+self.h) % self.h
            case = self.getPosition(xp, yp)

            if case[0] == None:
                #Si aucun agent on l'ajout dans les positions possibles
                res += [((xp, yp),case[1])]

        return res

    def canMove(self, x, y):
        return (self.getPosition(x,y)[0] == None)

    def appendAgent(self, agent, posX, posY):
        """
        Ajout un agent
        """
        self.setAgentPosition(agent, posX, posY)
        self.l_agents.append(agent)

    #########
    # DEBUG #
    #########

    def printGrid(self):
        for width in self.grid:
            for pos in width:
                print(str(pos),end='', flush=True)
            print(' ')
