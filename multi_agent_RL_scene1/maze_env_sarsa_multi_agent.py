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
import sys
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk


UNIT = 40   # pixels
MAZE_H = 10  # grid height
MAZE_W = 10  # grid width


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('Multi-agents Military Task')
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
        self._build_maze()

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='grey',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)

        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        # create origin
        origin = np.array([20, 20])

        # hell
        hell1_center = origin + np.array([UNIT * 4, UNIT])
        self.hell1 = self.canvas.create_rectangle(
            hell1_center[0] - 15, hell1_center[1] - 15,
            hell1_center[0] + 15, hell1_center[1] + 15,
            fill='black')
        # hell
        hell2_center = origin + np.array([UNIT, UNIT * 5])
        self.hell2 = self.canvas.create_rectangle(
            hell2_center[0] - 15, hell2_center[1] - 15,
            hell2_center[0] + 15, hell2_center[1] + 15,
            fill='black')
        
        # hell3_center = origin + np.array([UNIT * 2, UNIT * 2])
        # self.hell3 = self.canvas.create_rectangle(
        #     hell3_center[0] - 15, hell3_center[1] - 15,
        #     hell3_center[0] + 15, hell3_center[1] + 15,
        #     fill='black')

        # create oval 1
        oval1_center = origin + np.array([UNIT * 3, UNIT * 7])
        self.oval1 = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='yellow')
        
        # create oval 2
        oval2_center = origin + np.array([UNIT * 5, UNIT * 5])
        self.oval2 = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='yellow')
        
        
        # create oval 3
        oval3_center = origin + np.array([UNIT * 7, UNIT * 9])
        self.oval3 = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='yellow')
        
        self.done = np.array([0,0,0])

        # create red rect 1
        self.rect1 = self.canvas.create_oval(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')
        
        # create red rect 2
        self.rect2 = self.canvas.create_oval(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')
        
        # create red rect 3
        self.rect3 = self.canvas.create_oval(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')

        # pack all
        self.canvas.pack()

    def reset(self, visual=1):
        self.update()
        if visual == 1:
            time.sleep(0.5)
        self.canvas.delete(self.rect1)
        self.canvas.delete(self.rect2)
        self.canvas.delete(self.rect3)
        origin = np.array([20, 20])
        # create red rect 1
        self.rect1 = self.canvas.create_oval(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')
        
        # create red rect 2
        self.rect2 = self.canvas.create_oval(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')
        
        # create red rect 3
        self.rect3 = self.canvas.create_oval(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')
        ## Return the list of 3 observations
        return [self.canvas.coords(self.rect1), self.canvas.coords(self.rect2),self.canvas.coords(self.rect3)] 

    def step(self, action, TABLE):
        done = np.array([0,0,0])
        # step of s1
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

        s1_ = self.canvas.coords(self.rect1)  # next state
        # step of s2
        s2 = self.canvas.coords(self.rect2)
        #base_action = np.array([0, 0])
        if action == 0:   # up
            if s2[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:   # down
            if s2[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # right
            if s2[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:   # left
            if s2[0] > UNIT:
                base_action[0] -= UNIT

        self.canvas.move(self.rect2, base_action[0], base_action[1])  # move agent2
        
        s2_ = self.canvas.coords(self.rect2)  # next state
        # step of s3
        s3 = self.canvas.coords(self.rect3)
        #base_action = np.array([0, 0])
        if action == 0:   # up
            if s3[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:   # down
            if s3[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # right
            if s3[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:   # left
            if s3[0] > UNIT:
                base_action[0] -= UNIT

        self.canvas.move(self.rect3, base_action[0], base_action[1])  # move agent

        s3_ = self.canvas.coords(self.rect3)  # next state

        # reward function 1
        if s1_ == self.canvas.coords(self.oval1):
            reward1 = 1
            done[0] = True
            s1_ = 'terminal1'
        elif s1_ in [self.canvas.coords(self.oval2), self.canvas.coords(self.oval3)]:
            reward1 = 1
            if s1_ == self.canvas.coords(self.oval2):
                done[1] = True
                TABLE[1] = 0 # change the q_table of agent 2
                s1_ = 'terminal2'
            else:
                done[2] = True
                TABLE[2] = 0 # change the q_table of agent 3
                s1_ = 'terminal3'
        elif s1_ in [self.canvas.coords(self.hell1), self.canvas.coords(self.hell2)]:
            reward = -1
            #done[] = True
            s_ = 'terminal'
        else:
            reward = 0
            #done = False

        return s_, reward, done

    def render(self, visual=1):
        if visual == 1:
            time.sleep(0.1)
        self.update()