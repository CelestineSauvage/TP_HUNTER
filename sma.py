#coding: utf-8
from env import Env
from view import View
from tkinter import *
import random
import time
import json


from core.shark import Shark
from core.fish import Fish

from pprint import pprint

"""
Contient la méthode run() qui effectue le tour de parole
"""
class SMA:

    def __init__(self, nFishs, nSharks, fGestation, sGestation, sTime, l, h, size, limite, refresh, time, grid, displayGraph, sIntervale):

        #env
        self.env = Env(l, h, size, displayGraph,sIntervale)

        #n
        self.nSharks = nSharks
        self.nFishs = nFishs
        self.n = nSharks+nFishs

        #liste des agents
        self.env.generate(nSharks, Shark,[sGestation,sTime]) # liste des agents
        self.env.generate(nFishs, Fish,[fGestation]) # liste des agents

        self.view = View(l, h, size, self.env.l_agents, grid)

        #nb de tours
        self.nturn = 0
        self.limite = limite

        #refresh
        self.refresh = refresh

        # time
        self.time = time

        self.displayGraph = displayGraph
        self.sIntervale = sIntervale


    def turn(self):
        """
        Déroulement d'un tour
        """
        if (self.nturn == self.limite): # nb de tours < limite ?
            exit()
        self.env.removeDeadAgent()

        if(self.displayGraph):
            self.env.updateGraph()

        self.nturn+=1 # on incrémente le nombre de tour
        for i in range(0,self.refresh): # taux de refresh de la page
            # TOUR DE TOUS LES AGENTS
            for ag in self.env.l_agents:
                if(ag.life != 0):                
                    ag.decide(self.env)

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
    nSharks = 10
    nFishs = 10
    fGestation = 5
    sGestation = 5
    sTime = 3
    l = 100
    h = 100
    size = 10
    limite = -1
    refresh = 1
    time = 20
    grid = False
    displayGraph=False
    sIntervale=20

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
    if (data["nSharks"]):
        nSharks = int(data["nSharks"])
    if (data["nFishs"]):
        nFishs = int(data["nFishs"])
    if (data["fGestation"]):
        fGestation = int(data["fGestation"])
    if (data["sGestation"]):
        sGestation = int(data["sGestation"])
    if (data["sTime"]):
        sTime = int(data["sTime"])
    if (data["time"]):
        speed = int(data["time"])
    if (data["grid"]):
        grid = True
    if(data["displayGraph"]):
        displayGraph=True
    if(data["sIntervale"]):
        sIntervale=int(data["sIntervale"])

    game = SMA(nFishs,nSharks, fGestation, sGestation, sTime,
     l, h, size, limite, refresh, speed, grid, displayGraph, sIntervale)
    game.run()


if __name__ == "__main__":
    # execute only if run as a script
    main()
