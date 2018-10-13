# import sys,tty,termios
from threading import Thread, RLock
from pynput import keyboard

verrou = RLock()

#class _Getch:
#     def getch(self):
#             fd = sys.stdin.fileno()
#             old_settings = termios.tcgetattr(fd)
#             try:
#                 tty.setraw(sys.stdin.fileno())
#                 ch = sys.stdin.read(1)
#             finally:
#                 termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#             return ch

class KeyListener(Thread):

    def __init__(self, avatar):
        Thread.__init__(self)
        self.avatar = avatar
        # self.inkey = _Getch()

    def get(self, k):
        if k == keyboard.Key.up:
                self.change(1)
        elif k == keyboard.Key.down:
                self.change(0)
        elif k == keyboard.Key.right:
                self.change(3)
        elif k == keyboard.Key.left:
                self.change(2)
        else:
                pass
        #         sys.exit(0)

    def change(self, val):
        with verrou:
            self.avatar.on_press(val)

    def run(self):
            with keyboard.Listener(on_press=self.get) as listener:
                listener.join()
#         while(1):
#             self.get()