# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import os
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
    def __init__(self, name, xloc=0, yloc=0, atk_cast=0, size=20):
        self.name = name
        self.xloc = xloc
        self.yloc = yloc
        self.atk_cast = 0
        self.size = size
    
    
    def clone(self):
        return Player(self.name, self.xloc, self.yloc, self.atk_cast)

    
class Opponent:
    def __init__(self, targets, size=5, speed=1):
        self.size = size
        self.speed = speed
        self.tick_count = 0
        target = targets[0] # target = random.choice(targets) # warning: debug only
        self.xloc, self.yloc = get_random_border_location()
        self.ini_xloc, self.ini_yloc = self.xloc, self.yloc
        vec_x, vec_y = target.xloc - self.xloc, target.yloc - self.yloc
        reduce_factor = self.speed / distance(vec_x, vec_y)
        self.vec_x = vec_x * reduce_factor
        self.vec_y = vec_y * reduce_factor
        self.tick()
        
    
    def tick(self):
        next_x = int(self.ini_xloc + self.tick_count * self.vec_x)
        next_y = int(self.ini_yloc + self.tick_count * self.vec_y)
        if next_x < 0 or next_x > MAP_SIZE[0] or next_y < 0 or next_y > MAP_SIZE[1]:
            return 0
        self.xloc = next_x
        self.yloc = next_y
        self.tick_count += 1
        return 1 
        
        
def get_random_location():
    return (random.randint(0, MAP_SIZE[0]), random.randint(0, MAP_SIZE[1]))


def get_random_border_location():
    xory = random.randint(0, 1) # warning: probability doesnt rely on border size
    if xory:
        return (random.randint(0, MAP_SIZE[1 - xory]), MAP_SIZE[xory] * random.randint(0, 1))
    else:
        return (MAP_SIZE[xory] * random.randint(0, 1), random.randint(0, MAP_SIZE[1 - xory]))


def distance(x1, y1, x2=None, y2=None):
    if x2 is not None:
        x1 -= x2
    if y2 is not None:
        y1 -= y2
    return (x1**2 + y1**2)**.5


if __name__=="__main__":
    print("You're doing it wrong")
    
# -


