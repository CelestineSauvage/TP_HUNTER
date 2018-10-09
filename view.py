from tkinter import *

class View :

    def __init__(self, l, h, size, l_agents, grid):
        self.w = l*(size+1)
        self.h = h*(size+1)
        self.size = size

        #vue
        self.window = Tk()
        self.window.geometry(str(self.w)+"x"+str(self.h))

        #canvas
        self.canvas = Canvas(self.window, height=self.h, width=self.w,background='cyan')
        self.canvas.grid(row=1, column=1, sticky='w')
        self.grid = 0
        #self.window.configure(background='blue')
        if (grid):
            self.create_grid()
            self.grid = 0.5


    def create_grid(self, event=None):
        """
        Crée les lignes de la grille
        """
        # self.canvas.delete('grid_line') # Will only remove the grid_line

        # Creates all vertical lines at intevals of 100
        for i in range(0, self.w, self.size+1):
            self.canvas.create_line([(i, 0), (i, self.h)], tag='grid_line', fill='white')

        # Creates all horizontal lines at intevals of 100
        for i in range(0, self.h, self.size+1):
            self.canvas.create_line([(0, i), (self.w, i)], tag='grid_line', fill='white')

    def set_agent(self, time, l_agents, fct):
        """
        Bouge les ronds des agents
        """
        for agent in l_agents:
            x = agent.posX
            y = agent.posY
            isInit = self.isCanvasInit(agent)

            if(agent.life == 0):
                if isInit :
                    self.canvas.delete(agent.circle)
            else:
                if (isInit ):
                    if agent.getAge() == 2:
                        color = agent.getColor()
                        self.canvas.itemconfig(agent.circle, outline=color, fill=color)
                    self.canvas.coords(agent.circle, (x * self.size)+x + self.grid,
                                                        (y * self.size)+ y+ self.grid,
                                                        (x * self.size) + self.size + x - self.grid,
                                                        (y * self.size) + self.size + y - self.grid)
                else:
                    color = agent.getColorBorn()
                    agent.circle = self.canvas.create_rectangle([(x * self.size)+x+ self.grid,
                                                        (y * self.size)+ y+ self.grid,
                                                        (x * self.size) + self.size + x - self.grid,
                                                        (y * self.size) + self.size + y - self.grid],
                                                        outline=color, fill=color)
        self.window.after(time, fct)

    def isCanvasInit(self, agent):
        """

        """
        try:
            agent.circle
            return True
        except:
            return False

    def mainloop(self):
        self.window.mainloop()
