import sys
from threading import Thread, RLock
from pynput import keyboard

verrou = RLock()

class KeyListener(Thread):

    def __init__(self, avatar):
        Thread.__init__(self)
        self.avatar = avatar

    def get(self, k):
        if k == keyboard.Key.up:
                self.change(1)
        elif k == keyboard.Key.down:
                self.change(0)
        elif k == keyboard.Key.right:
                self.change(3)
        elif k == keyboard.Key.left:
                self.change(2)
        # else:
        #         print("Bye")
        #         sys.exit()

    def change(self, val):
        with verrou:
            self.avatar.on_press(val)

    def run(self):
            with keyboard.Listener(on_press=self.get) as listener:
                listener.join()
