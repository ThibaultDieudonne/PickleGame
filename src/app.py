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
from threading import Thread
import pygame
import pygbutton
import socket
import sys
import pickle
from util import Player, DataHandler, MAP_SIZE
import random

TICK_RATE = 60
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Client:
    def __init__(self):
        self.in_game = False
        self.has_to_run = True
        self.menu_size = (115, 75)
        self.screen_size = MAP_SIZE
        self.buffer = []
        self.step = 8
        self.ip = None
        self.port = None
        self.name = None
        self.socket = None
        self.game_data = DataHandler()
        with open('game.cfg', 'rb') as f:
            config = f.readlines()
        for line in config:
            tmp = line.decode("utf-8").replace('\n', '').replace('\r', '').replace(' ', '').split(':')
            if len(tmp) == 2:
                if tmp[0] == "ip":
                    self.ip = tmp[1]
                elif tmp[0] == "port":
                    self.port = int(tmp[1])
                elif tmp[0] == "name":
                    self.name = tmp[1] + "#" + str(random.randint(1000, 9999))
        if self.ip is None or self.port is None or self.name is None:
            raise Exception("Missing ip, port or name in game.cfg")
        else:
            print(f'[{self.name}@{self.ip}:{self.port}]')
                       
    def display(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Pickle Game")
        self.font = pygame.font.SysFont('Berlin Sans FB', 30)
        self.screen = pygame.display.set_mode(self.menu_size)
        self.clock = pygame.time.Clock()
        self.screen.fill((0, 0, 0))
        self.bplay = pygbutton.PygButton((20, 20, 75, 35), 'Play !')
        
        while self.has_to_run:
            pygame.display.update()
            self.clock.tick(TICK_RATE)
            self.screen.fill((0, 0, 0))
            if self.in_game:
                candidate_player = self.game_data.players[self.game_data.indexes[self.name]].clone()
                for ctrl in self.buffer:
                    if ctrl == 0:
                        candidate_player.ypos = max(0, candidate_player.ypos - self.step)
                    elif ctrl == 1:
                        candidate_player.ypos = min(self.screen_size[1], candidate_player.ypos + self.step)
                    elif ctrl == 2:
                        candidate_player.xpos = max(0, candidate_player.xpos - self.step)
                    elif ctrl == 3:
                        candidate_player.xpos = min(self.screen_size[0], candidate_player.xpos + self.step)
                self.send_and_update(candidate_player)
                pygame.draw.circle(self.screen, BLUE, (self.game_data.players[0].xpos, self.game_data.players[0].ypos), 20)
                pygame.draw.circle(self.screen, RED, (self.game_data.players[1].xpos, self.game_data.players[1].ypos), 20)
            else:
                self.bplay.draw(self.screen)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.has_to_run = False
                if self.in_game:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.buffer.append(0)
                        if event.key == pygame.K_DOWN:
                            self.buffer.append(1)
                        if event.key == pygame.K_LEFT:
                            self.buffer.append(2)
                        if event.key == pygame.K_RIGHT:
                            self.buffer.append(3)
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_UP:
                            self.buffer.remove(0)
                        if event.key == pygame.K_DOWN:
                            self.buffer.remove(1)
                        if event.key == pygame.K_LEFT:
                            self.buffer.remove(2)
                        if event.key == pygame.K_RIGHT:
                            self.buffer.remove(3)
                else:
                    if 'click' in self.bplay.handleEvent(event):
                        self.in_game = True
                        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.socket.connect((self.ip, self.port))
                        self.send_and_update(self.name)
                        self.screen = pygame.display.set_mode(self.screen_size)
        
        
    def send_and_update(self, packet):
        if isinstance(packet, str):
            packet = bytes(packet, "utf-8")
        else:
            packet = pickle.dumps(packet)
        self.socket.send(packet)
        tmp_data = pickle.loads(self.socket.recv(1024))
        self.game_data = tmp_data

    
    def __del__(self):
        if self.socket is not None:
            self.socket.close()
        
                
if __name__=="__main__":
    client = Client()
    client.display()
# -




