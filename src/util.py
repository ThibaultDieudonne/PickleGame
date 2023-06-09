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


class GameState:
    def __init__(self):
        self.players = []
        self.indexes = {}
        self.opponents = []


class Stage:
    def __init__(self):
        self.upgrade_frq = 1000
        self.ticks = 0
        self.current = 0
        self.spawn_frqs = [100, 50, 25, 15, 10, 5]
        self.opp_speeds = [1, 2, 4, 6, 8, 10]
        self.tick_time = .01

    def get_opp(self):
        if self.ticks % self.spawn_frqs[self.current]:
            return 0
        return self.opp_speeds[self.current]

    
    def tick(self):
        time.sleep(self.tick_time)
        self.ticks += 1
        if not (self.ticks % self.upgrade_frq):
            self.current = min(len(self.spawn_frqs) - 1, self.current + 1)
        
        
class Player:
    def __init__(self, name, xloc=0, yloc=0, size=20, speed=8, damage_taken=0, active=1, score=0):
        self.name = name
        self.xloc = xloc
        self.yloc = yloc
        self.size = size
        self.speed = 8
        self.damage_taken = damage_taken
        self.active = active
        self.score = score
    
    
    def update(self, client_query):
        self.xloc = client_query.xloc
        self.yloc = client_query.yloc

    
class ClientQuery:
    def __init__(self, player):
        self.xloc = player.xloc
        self.yloc = player.yloc
        
    
class Opponent:
    def __init__(self, targets, size=5, speed=1, damage=10):
        self.size = size
        self.speed = speed
        self.damage = damage
        self.tick_count = 0
        target = random.choice(targets)
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


