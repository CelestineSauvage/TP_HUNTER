import sys,tty,termios
from threading import Thread, RLock
 verrou = RLock()
 class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(3)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch
 class KeyListener(Thread):
     def __init__(self, avatar):
        Thread.__init__(self)
        self.avatar = avatar
     def get(self):
            inkey = _Getch()
            while(1):
                    k=inkey()
                    if k!='':break
            if k=='\x1b[A':
                    print("up")
                    self.change(1)
            elif k=='\x1b[B':
                    print("down")
                    self.change(0)
            elif k=='\x1b[C':
                    print("right")
                    self.change(3)
            elif k=='\x1b[D':
                    print ("left")
                    self.change(2)
            else:
                    print("Bye")
                    sys.exit(0)
     def change(self, val):
        with verrou:
            self.avatar.on_press(val)
     def run(self):
        while(1):
            self.get()