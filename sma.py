#coding: utf-8
from env import Env
from view import View

from tkinter import *
import random
import time
import json


from core.Hunter import Hunter
from core.Avatar import Avatar
from core.Wall import Wall


from pprint import pprint

"""
Contient la méthode run() qui effectue le tour de parole
"""
class SMA:

    def __init__(self, l, h, size, limite, refresh, time, grid, nHunter):

        #env
        self.env = Env(l, h, size)

        #n
        #liste des agents
        self.env.generate(1, Avatar)

        self.env.generate(nHunter, Hunter, [1])
        self.generate_maze()
        # self.env.generate((l*h//6), Wall) # 1/6ème de la map est occupée par des murs

        self.view = View(l, h, size, self.env.l_agents)

        #nb de tours
        self.nturn = 0
        self.limite = limite

        #refresh
        self.refresh = refresh

        # time
        self.time = time

    def generate_maze (self):
        chamber = [(1, 1),(self.env.l-1, 1),(self.env.l-1, self.env.h-1),(1, self.env.h-1)]
        l_walls = self.rec_generate_maze(chamber, [], [], 4)
        self.env.generate2(l_walls, Wall)

    def rec_generate_maze(self, chamber, l_vide, h_vide, minsize):
        ll = chamber[0][0]
        lr = chamber[1][0]
        hl = chamber[0][1]
        hr = chamber[2][1]

        l = lr - ll #example (0, 0),(self.l, 0) -> l - 0
        h = hr - hl #example (0, 0),(self.l, 0),(self.l, self.h)) -> h - 0

        if (l*h < minsize) :
            return []
        else :
            l_walls = []
            newl_vide = []
            newh_vide = []
            #traçage verticale
            l2 = random.randint(ll, lr)

            #traçage horizontale
            h2 = random.randint(hl, hr)
            jct = (l2, h2) # jonction des 2 lignes

            for i in range (hl, hr): # parcours vertical pour définir les murs ou non
                if (not(i in h_vide)):
                    wall = random.randint(0,4)
                    if (wall > 0):
                        l_walls += [(l2, i)]
                    else :
                        newh_vide += [i]

            for j in range (ll, lr): # parcours horizontal pour définir les murs ou non
                if (not(j in l_vide)):
                    wall = random.randint(0,4)
                    if (wall > 0):
                        l_walls += [(j, h2)]
                    else :
                        newl_vide += [j]

            # on calcule récursivement dans les 4 nouvelles cases les murs à placer

            # en haut à gauche
            l_walls += self.rec_generate_maze([(ll,hl), (l2-1,hl), (l2-1,h2-1), (ll,h2-1)], newl_vide, newh_vide, minsize)

            # # en haut à droite
            l_walls += self.rec_generate_maze([(l2+1,hl+1), (lr,hl+1), (lr,h2), (l2+1,h2)], newl_vide, newh_vide, minsize)
            #
            # # en bas à droite
            l_walls += self.rec_generate_maze([(l2+1,h2+1), (lr,h2+1), (lr,hr), (l2+1,hr)], newl_vide, newh_vide, minsize)
            #
            # # en bas à gauche
            l_walls += self.rec_generate_maze([(ll,h2), (l2-1,h2), (l2-1,hr-1), (ll,hr-1)], newl_vide, newh_vide, minsize)

            return l_walls


    def turn(self):
        """
        Déroulement d'un tour
        """

        # nb de tours < limite ?
        if (self.nturn == self.limite):
            exit()

        self.nturn+=1 # on incrémente le nombre de tour
        self.env.removeDeadAgent()
        for i in range(0,self.refresh): # taux de refresh de la page
            # TOUR DE TOUS LES AGENTS
            for ag in self.env.l_agents:
                if(ag.life != 0):
                    ag.decide(self.env)

        self.env.printGrid()
        self.view.set_agent(self.time, self.env.l_agents, self.turn)

    def run(self):

        self.view.set_agent(self.time, self.env.l_agents, self.turn)
        self.view.mainloop()

def parse():
    """
    Parse le fichier JSON de config
    """
    with open('Properties.json') as data_file:
        data = json.load(data_file)
        return data

def main():
    data = parse()

    # set des valeurs par défault
    l = 100
    h = 100
    size = 10
    limite = -1
    refresh = 1
    time = 20
    grid = False
    sHunter=2

    # parcours des options saisis par l'utilisateur
    if (data["gridSizeX"]):
        l = int(data["gridSizeX"])
    if (data["gridSizeY"]):
        h = int(data["gridSizeY"])
    if (data["boxSize"]):
        size = int(data["boxSize"])
    if (data["scheduling"]):
        action = int(data["scheduling"])
    if (data["nbTicks"]):
        limite = int(data["nbTicks"])
    if (data["seed"]):
        random.seed(int(data["seed"]))
    if (data["refresh"]):
        refresh = int(data["refresh"])
    if (data["time"]):
        speed = int(data["time"])
    if (data["grid"]):
        grid = True
    if(data["sHunter"]):
        sHunter=int(data["sHunter"])

    game = SMA(l, h, size, limite, refresh, speed, grid, sHunter)
    game.run()


if __name__ == "__main__":
    # execute only if run as a script
    main()
