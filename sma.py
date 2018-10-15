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
        self.env.generate((l*h//6), Wall) # 1/6ème de la map est occupée par des murs

        self.view = View(l, h, size, self.env.l_agents)

        #nb de tours
        self.nturn = 0
        self.limite = limite

        #refresh
        self.refresh = refresh

        # time
        self.time = time

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
