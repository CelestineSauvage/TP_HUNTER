from core.Agent import Agent
from pynput import keyboard

"""
"""
class Avatar(Agent):
    def __init__(self, posX, posY, data=[]):
        # position initiale de la particule
        super(Avatar, self).__init__(posX, posY)
        self.vector = (1,1)

        #Start du thread en parallèle
        with keyboard.Listener(
                on_press=self.on_press) as listener:
            listener.join()

    def decide(self, env):
        """

        """
        xp, yp = (posX+self.vector[0]+env.l) % env.l, (posY+self.vector[0]+env.h) % env.h
        env.setAgentPosition(self, newPos[0], newPos[1])

    def getColor(self):
        """
        """
        return "yellow"

    def on_press(self, key):
        #On change le vector du pac man
        try:
            if key == keyboard.Key.up:
                self.vector = (self.vector[0], 1)
            elif key == keyboard.Key.down:
                self.vector = (self.vector[0], -1)
            elif key == keyboard.Key.left:
                self.vector = (-1, self.vector[1])
            elif key == keyboard.Key.right:
                self.vector = (1, self.vector[1])
        except AttributeError:
            print('special key {0} pressed'.format(
                key))