"""
Reinforcement learning maze example.
Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].
This script is the environment part of this example.
The RL is in RL_brain.py.
View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""


import numpy as np
import time
#import sys
import tkinter as tk
import os


UNIT = 40   # pixels
MAZE_H = 10  # grid height
MAZE_W = 10  # grid width

# image_file = tk.PhotoImage(file='UAV_1.gif')
# global UAV_1 = tk.canvas.create_image(20, 30, anchor='nw', image=image_file)
# global UAV_2 = tk.canvas.create_image(20, 30, anchor='nw', image=image_file)
# global UAV_3 = tk.canvas.create_image(20, 30, anchor='nw', image=image_file)


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'r', 'l']
        self.n_actions = len(self.action_space)
        self.title('MAPP Simulation System v1.0')
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
        self.iconbitmap(os.path.join(os.path.dirname(__file__),'HITlogoblue.ico'))
        self._build_maze()
        self.termi = ['terminal1','terminal2','terminal3','terminal']
        #global self.UAV_1

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='SpringGreen', #SpringGreen
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)

        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1, fill = 'red', dash = (4,4))
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1,fill = 'blue', dash = (4,4))

        # create origin
        origin = np.array([20, 20])

        # hell
        hell1_center = origin + np.array([UNIT * 4, UNIT])
        self.hell1 = self.canvas.create_rectangle(
            hell1_center[0] - 15, hell1_center[1] - 15,
            hell1_center[0] + 15, hell1_center[1] + 15,
            fill='grey')
        # hell
        hell2_center = origin + np.array([UNIT*5, UNIT * 5])
        self.hell2 = self.canvas.create_rectangle(
            hell2_center[0] - 15, hell2_center[1] - 15,
            hell2_center[0] + 15, hell2_center[1] + 15,
            fill='grey')
        
        hell3_center = origin + np.array([UNIT * 2, UNIT * 8])
        self.hell3 = self.canvas.create_rectangle(
            hell3_center[0] - 15, hell3_center[1] - 15,
            hell3_center[0] + 15, hell3_center[1] + 15,
            fill='grey')

        # create oval 1
        global MBase_image 
        MBase_image = tk.PhotoImage(file = os.path.join(os.path.dirname(__file__),'MBase.gif'))
        oval1_center = origin + np.array([UNIT * 8, UNIT * 2])
        self.oval1 = self.canvas.create_rectangle(
            oval1_center[0] - 15, oval1_center[1] - 15,
            oval1_center[0] + 15, oval1_center[1] + 15,
            fill='',outline = '')
        self.MBase1 = self.canvas.create_image(oval1_center[0], oval1_center[1], anchor='center',image=MBase_image)
        
        # create oval 2
        oval2_center = origin + np.array([UNIT * 9, UNIT * 5])
        self.oval2 = self.canvas.create_rectangle(
            oval2_center[0] - 15, oval2_center[1] - 15,
            oval2_center[0] + 15, oval2_center[1] + 15,
            fill='',outline = '')
        self.MBase2 = self.canvas.create_image(oval2_center[0], oval2_center[1], anchor='center',image=MBase_image)
        
        
        # create oval 3
        oval3_center = origin + np.array([UNIT * 5, UNIT * 8])
        self.MBase3 = self.canvas.create_image(oval3_center[0], oval3_center[1], anchor='center',image=MBase_image)
        self.oval3 = self.canvas.create_rectangle(
            oval3_center[0] - 15, oval3_center[1] - 15,
            oval3_center[0] + 15, oval3_center[1] + 15,
            fill='',outline = '')
        
        
        self.done = np.array([0,0,0])

        # create red rect 1
        image_file = tk.PhotoImage(file = os.path.join(os.path.dirname(__file__),'UAV_1.gif'))
        self.UAV_1 = self.canvas.create_image(20, 20, anchor='center',image=image_file)
        rect1_center = origin + np.array([0, 0])
        self.rect1 = self.canvas.create_oval(
            rect1_center[0] - 15, rect1_center[1] - 15,
            rect1_center[0] + 15, rect1_center[1] + 15,
            fill='',outline = '')
        
        
        # create red rect 2
        #image_file = tk.PhotoImage(file='UAV_1.gif')
        self.UAV_2 = self.canvas.create_image(20, 20+UNIT*3,anchor='center', image=image_file)
        rect2_center = origin + np.array([0, UNIT * 3])
        self.rect2 = self.canvas.create_oval(
            rect2_center[0] - 15, rect2_center[1] - 15,
            rect2_center[0] + 15, rect2_center[1] + 15,
            fill='',outline = '')
        
        
        # create red rect 3
        #image_file = tk.PhotoImage(file='UAV_1.gif')
        self.UAV_3 = self.canvas.create_image(20, 20+UNIT*6,anchor='center', image=image_file)
        rect3_center = origin + np.array([0, UNIT * 6])
        self.rect3 = self.canvas.create_oval(
            rect3_center[0] - 15, rect3_center[1] - 15,
            rect3_center[0] + 15, rect3_center[1] + 15,
            fill='',outline = '')
        

        # pack all
        self.canvas.pack()

    def reset(self, visual=1):
        self.update()
        if visual == 1:
            time.sleep(0.5)
        self.canvas.delete(self.rect1)
        self.canvas.delete(self.rect2)
        self.canvas.delete(self.rect3)
        self.canvas.delete(self.UAV_1)
        self.canvas.delete(self.UAV_2)
        self.canvas.delete(self.UAV_3)
        global MBase_image
        MBase_image = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__),'MBase.gif'))
        origin = np.array([20, 20])
        # creat oval 1
        oval1_center = origin + np.array([UNIT * 8, UNIT * 2])
        self.MBase1 = self.canvas.create_image(oval1_center[0], oval1_center[1], anchor='center',image=MBase_image)
        
        # create oval 2
        oval2_center = origin + np.array([UNIT * 9, UNIT * 5])
        self.MBase2 = self.canvas.create_image(oval2_center[0], oval2_center[1], anchor='center',image=MBase_image)
        
        # create oval 3
        oval3_center = origin + np.array([UNIT * 5, UNIT * 8])
        
        self.MBase3 = self.canvas.create_image(oval3_center[0], oval3_center[1], anchor='center',image=MBase_image)
        
        # create red rect 1
        global image_file
        image_file = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__),'UAV_1.gif'))

        
        rect1_center = origin + np.array([0, 0])
        self.rect1 = self.canvas.create_oval(
            rect1_center[0] - 15, rect1_center[1] - 15,
            rect1_center[0] + 15, rect1_center[1] + 15,
            fill='',outline = '')
        self.UAV_1 = self.canvas.create_image(20, 20, anchor='center',image=image_file)
        
        
        # create red rect 2
        
        rect2_center = origin + np.array([0, UNIT * 3])
        self.rect2 = self.canvas.create_oval(
            rect2_center[0] - 15, rect2_center[1] - 15,
            rect2_center[0] + 15, rect2_center[1] + 15,
            fill='',outline = '')
        self.UAV_2 = self.canvas.create_image(20, 20+UNIT*3,anchor='center', image=image_file)
        
        
        # create red rect 3
        #image_file = tk.PhotoImage(file='UAV_1.gif')
        
        rect3_center = origin + np.array([0, UNIT * 6])
        self.rect3 = self.canvas.create_oval(
            rect3_center[0] - 15, rect3_center[1] - 15,
            rect3_center[0] + 15, rect3_center[1] + 15,
            fill='',outline = '')
        self.UAV_3 = self.canvas.create_image(20, 20+UNIT*6, anchor='center', image=image_file)
        
        ## Return the list of 3 observations
        return[self.canvas.coords(self.rect1), self.canvas.coords(self.rect2),self.canvas.coords(self.rect3)]

    def step(self, bot, action):
        # done = np.array([0,0,0])
        index_goal = 0
        reward = 0
        #reward1 = 0
        # step of s1
        if bot == 0:
            s1 = self.canvas.coords(self.rect1)
            base_action = np.array([0, 0])
            if action == 0:   # up
                if s1[1] > UNIT:
                    base_action[1] -= UNIT
            elif action == 1:   # down
                if s1[1] < (MAZE_H - 1) * UNIT:
                    base_action[1] += UNIT
            elif action == 2:   # right
                if s1[0] < (MAZE_W - 1) * UNIT:
                    base_action[0] += UNIT
            elif action == 3:   # left
                if s1[0] > UNIT:
                    base_action[0] -= UNIT

            self.canvas.move(self.rect1, base_action[0], base_action[1])  # move agent1
            self.canvas.move(self.UAV_1, base_action[0], base_action[1])
            if s1 not in self.termi:
                s1_ = self.canvas.coords(self.rect1)  # next state
            else:
                s1_=s1
                
            # compute reward and index_bot and index_goal
            if s1_ == self.canvas.coords(self.oval1):
                reward = 1
                index_goal = 1
                #s1_ = s1
        
            elif s1_ in [self.canvas.coords(self.oval2), self.canvas.coords(self.oval3)]:
                reward = 1
                if s1_ == self.canvas.coords(self.oval2):
                    index_goal = 2
                    #s1_ = 'terminal2'
                else:
                    index_goal = 3
                    #s1_ = 'terminal3'
            elif s1_ in [self.canvas.coords(self.hell1), self.canvas.coords(self.hell2),self.canvas.coords(self.hell3)]:
                reward = -1
                #s1_ = 'terminal'
                #done = False
            return s1_, reward, index_goal
        # Step of s2: 
        elif bot == 1:
            s = self.canvas.coords(self.rect2)
            base_action = np.array([0, 0])
            if action == 0:   # up
                if s[1] > UNIT:
                    base_action[1] -= UNIT
            elif action == 1:   # down
                if s[1] < (MAZE_H - 1) * UNIT:
                    base_action[1] += UNIT
            elif action == 2:   # right
                if s[0] < (MAZE_W - 1) * UNIT:
                    base_action[0] += UNIT
            elif action == 3:   # left
                if s[0] > UNIT:
                    base_action[0] -= UNIT

            self.canvas.move(self.rect2, base_action[0], base_action[1])  # move agent1
            self.canvas.move(self.UAV_2, base_action[0], base_action[1])
            if s not in self.termi:
                s_ = self.canvas.coords(self.rect2)  # next state
            else:
                s_=s
                
            # compute reward and index_bot and index_goal
            if s_ == self.canvas.coords(self.oval2):
                reward = 1
                index_goal = 2
                #s_ = 'terminal2'
        
            elif s_ in [self.canvas.coords(self.oval1), self.canvas.coords(self.oval3)]:
                reward = 1
                if s_ == self.canvas.coords(self.oval1):
                    index_goal = 1
                    #s_ = 'terminal1'
                else:
                    index_goal = 3
                    #s_ = 'terminal3'
            elif s_ in [self.canvas.coords(self.hell1), self.canvas.coords(self.hell2), self.canvas.coords(self.hell3)]:
                reward = -1
                #s_ = 'terminal'
            else:
                reward = 0
                #done = False
            return s_, reward, index_goal
        # Step of s3: 
        elif bot == 2:
            s = self.canvas.coords(self.rect3)
            base_action = np.array([0, 0])
            if action == 0:   # up
                if s[1] > UNIT:
                    base_action[1] -= UNIT
            elif action == 1:   # down
                if s[1] < (MAZE_H - 1) * UNIT:
                    base_action[1] += UNIT
            elif action == 2:   # right
                if s[0] < (MAZE_W - 1) * UNIT:
                    base_action[0] += UNIT
            elif action == 3:   # left
                if s[0] > UNIT:
                    base_action[0] -= UNIT

            self.canvas.move(self.rect3, base_action[0], base_action[1])  # move agent1
            self.canvas.move(self.UAV_3, base_action[0], base_action[1])
            if s not in self.termi:
                s_ = self.canvas.coords(self.rect3)  # next state
            else:
                s_=s
                
            # compute reward and index_bot and index_goal
            if s_ == self.canvas.coords(self.oval3):
                reward = 1
                index_goal = 3
                #s_ = 'terminal3'
        
            elif s_ in [self.canvas.coords(self.oval1), self.canvas.coords(self.oval2)]:
                reward = 1
                if s_ == self.canvas.coords(self.oval1):
                    index_goal = 1
                    #s_ = 'terminal1'
                else:
                    index_goal = 2
                    #s_ = 'terminal2'
            elif s_ in [self.canvas.coords(self.hell1), self.canvas.coords(self.hell2)]:
                reward = -1
                #s_ = 'terminal'
                index_goal = 0
            else:
                reward = 0
                index_goal = 0
                #done = False
            return s_, reward, index_goal

        
    def render(self, visual=1):
        if visual == 1:
            time.sleep(0.1)
        self.update()