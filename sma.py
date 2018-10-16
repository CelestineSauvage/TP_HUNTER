#coding: utf-8
from env import Env
from view import View

from tkinter import *
import random
import time
import json
import sys


from core.Hunter import Hunter
from core.Avatar import Avatar
from core.Defender import Defender
from core.Winner import Winner
from core.Wall import Wall
from getch import KeyListener
from pynput import keyboard



from pprint import pprint

"""
Contient la méthode run() qui effectue le tour de parole
"""
class SMA:

    def __init__(self, l, h, size, limite, refresh, time, grid, nHunter, speedAvatar, speedHunter, defenderLife, perc):

        #env
        self.env = Env(l, h, size)

        #n
        #liste des agents
        if (perc != 1):
            self.env.generate((l*h*perc)//100, Wall) # 1/6ème de la map est occupée par des murs
        else :
            self.generate_maze()

        self.env.generate(1, Avatar, [speedAvatar])

        self.env.generate(nHunter, Hunter, [speedHunter])

        self.view = View(l, h, size, self.env.l_agents)

        #nb de tours
        self.nturn = 0
        self.limite = limite

        #refresh
        self.refresh = refresh

        # time
        self.time = time

        self.defenderLife = defenderLife
        self.nbDefender = 0
        self.winner = False
        self.pause = False

        self.keyL = KeyListener(self)
        self.keyL.start()


    def generate_maze (self):
        l_grille = [[False] * (self.env.h) for _ in range(self.env.l)]
        x = random.randint(0, self.env.l-1)
        y = random.randint(0, self.env.h-1)

        l_grille[x][y] = True

        vector = [(0,-2), (2,0), (0,2), (-2,0)]
        l_walls = []
        for v in vector:
            px = (x+v[0]+self.env.l) % self.env.l
            py = (y+v[1]+self.env.h) % self.env.h
            l_walls.append((px,py))

        while (len(l_walls) != 0):
            r = random.randint(0, len(l_walls)-1)
            wall = l_walls[r]
            l_walls.remove(wall)

            random.shuffle(vector)

            for v in vector:
                px = (wall[0]+v[0]+self.env.l) % self.env.l
                py = (wall[1]+v[1]+self.env.h) % self.env.h

                if l_grille[px][py]:
                    l_grille[wall[0]][wall[1]] = True

                    #On détruit le mur entre les deux cases du laby
                    px2 = (wall[0] + (v[0]//2) +self.env.l) % self.env.l
                    py2 = (wall[1] + (v[1]//2) +self.env.h) % self.env.h
                    # print("-------")
                    # print((px,py))
                    # print((wall))
                    # print(v)
                    # print((px2,py2))
                    # print((v[0]//2), (v[1]//2))
                    l_grille[px2][py2] = True

                    # On ajoute ses voisins qui n'appartiennent pas au laby
                    for v in vector:
                        px = (wall[0]+v[0]+self.env.l) % self.env.l
                        py = (wall[1]+v[1]+self.env.h) % self.env.h

                        if not l_grille[px][py]:
                            if (not (px,py) in l_walls):
                                l_walls.append((px,py))
                    break


        self.env.generate2(l_grille, Wall)
        # chamber = [(0, 0),(self.env.l-1, 0),(self.env.l-1, self.env.h-1),(0, self.env.h-1)]
        # l_walls = self.rec_generate_maze(chamber, [], [], 3)
        # self.env.generate2(l_walls, Wall)

    # def rec_generate_maze(self, chamber, l_vide, h_vide, minsize):

        # ll = chamber[0][0]
        # lr = chamber[1][0]
        # hl = chamber[0][1]
        # hr = chamber[2][1]
        #
        # l = lr - ll #example (0, 0),(self.l, 0) -> l - 0
        # h = hr - hl #example (0, 0),(self.l, 0),(self.l, self.h)) -> h - 0
        #
        # if ((l*h) < minsize or (l < minsize ) or (h < minsize)) :
        #     return []
        # else :
        #     l_walls = []
        #     newl_vide = []
        #     newh_vide = []
        #     # jct = (l2, h2) # jonction des 2 lignes
        #     #traçage verticale
        #
        #     h2 = random.randint(hl+2, hr-1)
        #     for j in range (ll, lr): # parcours horizontal pour définir les murs ou non
        #         if (not(j in l_vide)):
        #             wall = random.randint(0,h//2)
        #             if (wall > 0):
        #                 l_walls += [(j, h2)]
        #             else :
        #                 newh_vide += [j]
        #
        #
        #     l2 = random.randint(ll+2, lr-1)
        #     for i in range (hl, hr): # parcours vertical pour définir les murs ou non
        #         if (not(i in h_vide)):
        #             wall = random.randint(0,l//2)
        #             if (wall > 0):
        #                 l_walls += [(l2, i)]
        #             else :
        #                 newl_vide += [i]
        #
        #
        #
        #
        #     # on calcule récursivement dans les 4 nouvelles cases les murs à placer
        #
        #     # en haut à gauche
        #     l_walls += self.rec_generate_maze([(ll,hl), (l2,hl), (l2,h2), (ll,h2)], l_vide + newl_vide, h_vide + newh_vide, minsize)
        #
        #     # # en haut à droite
        #     l_walls += self.rec_generate_maze([(l2,hl), (lr,hl), (lr,h2), (l2,h2)], l_vide + newl_vide, h_vide + newh_vide, minsize)
        #     # #
        #     # # en bas à droite
        #     l_walls += self.rec_generate_maze([(l2,h2), (lr,h2), (lr,hr), (l2,hr)], newl_vide, newh_vide, minsize)
        #     #
        #     # # en bas à gauche
        #     l_walls += self.rec_generate_maze([(ll,h2), (l2,h2), (l2,hr), (ll,hr)], newl_vide, newh_vide, minsize)
        #
        #     return l_walls


    def turn(self):
        """
        Déroulement d'un tour
        """
        if not self.pause:
            # nb de tours < limite ?
            if (self.nturn == self.limite):
                exit()

            if not (self.nturn % self.defenderLife) and self.nbDefender<4:
                self.env.generate(1, Defender, [self.defenderLife])
            elif self.nbDefender == 4 and not self.winner:
                self.winner = True
                self.env.generate(1, Winner)

            self.nturn+=1 # on incrémente le nombre de tour
            dead = self.env.removeDeadAgent()

            #On parcours les agent pour voir si un defender est mort
            for agent in dead:
                if agent.getType() == 3 and not agent.natural:
                    self.nbDefender +=1
                    for agent in self.env.l_agents:
                        agent.fearMode = True
                if agent.getType() == 0 or agent.getType() ==4:
                    self.view.window.destroy()
                    self.keyL.stop()
                    sys.exit(0)
            for i in range(0,self.refresh): # taux de refresh de la page
                # TOUR DE TOUS LES AGENTS
                for ag in self.env.l_agents:
                    if(ag.isAlive()):
                        ag.decide(self.env)

        self.view.set_agent(self.time, self.env.l_agents, self.turn)
    def run(self):
        self.view.set_agent(self.time, self.env.l_agents, self.turn)
        self.view.mainloop()

    def on_press(self, key):
        if key == keyboard.KeyCode.from_char('w'):
            if(self.time>100):
                self.time -= 100
            else:
                self.time = 50
        elif key == keyboard.KeyCode.from_char('x'):
            self.time +=100
        elif key == keyboard.Key.space:
            self.pause = not self.pause
        else:
            for agent in self.env.l_agents:
                agent.on_press(key)

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
    speedAvatar = 1
    speedHunter = 1
    defenderLife = 2
    perc = 1

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
    if data["SpeedAvatar"]:
        speedAvatar = int(data["SpeedAvatar"])
    if data["SpeedHunter"]:
        speedHunter = int(data["SpeedHunter"])
    if data["DefenderLife"]:
        defenderLife = int(data["DefenderLife"])
    if data["perc"]:
        perc = int(data["perc"])

    game = SMA(l, h, size, limite, refresh, speed, grid, sHunter, speedAvatar, speedHunter, defenderLife, perc)

    game.run()


if __name__ == "__main__":
    # execute only if run as a script
    main()
