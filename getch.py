import sys
from threading import Thread, RLock
from pynput import keyboard

verrou = RLock()

class KeyListener(Thread):

    def __init__(self, sma):
        Thread.__init__(self)
        self.sma = sma

    def get(self, k):
        self.change(k)

    def change(self, val):
        with verrou:
                self.sma.on_press(val)

    def run(self):
            with keyboard.Listener(on_press=self.get) as listener:
                listener.join()