import sys
import random
import time
import pickle
import socket
from threading import Thread

MAP_SIZE = (1024, 512)
BUFFER_SIZE = 16384
STEP = 8

class DataHandler:
    def __init__(self):
        self.players = []
        self.indexes = {}
        self.opponents = []

class Player:
    def __init__(self, name, xloc=0, yloc=0, atk_cast=0):
        self.name = name
        self.xloc = xloc
        self.yloc = yloc
        self.atk_cast = 0

    def args_count(self):
        return len(vars(self))
    
    def clone(self):
        return Player(self.name, self.xloc, self.yloc, self.atk_cast)
    
    def packet(self):
        vrs = vars(self)
        return SEP_CHAR.join([str(vrs[v])for v in vrs])

class Opponent:
    def __init__(self, targets, size=5, speed=1):
        self.active = 1
        self.current_tick = -1
        self.size = size
        self.speed = speed
        target = random.choice(targets)
        xloc = random.randint(size, MAP_SIZE[0] - size)
        yloc = random.randint(size, MAP_SIZE[1] - size)
        traj_lead = (target.yloc - yloc) / (target.xloc - xloc)
        traj_flat = target.yloc - target.xloc * traj_lead
        self.trajectory = []
        for moving_x in range(0, MAP_SIZE[0], STEP):
            moving_y = int(traj_lead * moving_x + traj_flat)
            if moving_y >= 0 and moving_y <= MAP_SIZE[1]:
                self.trajectory.append((moving_x, moving_y))
        if random.randint(0, 1):
            self.trajectory = self.trajectory[::-1]
        self.tick()
    
    def tick(self):
        self.current_tick += 1
        if self.current_tick == len(self.trajectory):
            return 0
        self.xloc = self.trajectory[self.current_tick][0]
        self.yloc = self.trajectory[self.current_tick][1]
        return 1
        

