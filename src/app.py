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

class Interface:
    def __init__(self):
        self.in_game = False
        self.has_to_run = True
        self.menu_size = (574, 232)
        self.screen_size = (1366, 768)
        self.step = 50
        self.ip = None
        self.port = None
        self.name = None
        with open('game.cfg', 'rb') as f:
            config = f.readlines()
        for line in config:
            tmp = line.decode("utf-8").replace('\n', '').replace(' ', '').split(':')
            if len(tmp) == 2:
                if tmp[0] == "ip":
                    self.ip = tmp[1]
                elif tmp[0] == "port":
                    self.port = int(tmp[1])
                elif tmp[0] == "name":
                    self.name = tmp[1]
        if self.ip is None or self.port is None or self.name is None:
            raise Exception("Missing ip, port or name in game.cfg")
                    
        
        
    def display(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Pickle Game")
        self.font = pygame.font.SysFont('Berlin Sans FB', 30)
        self.screen = pygame.display.set_mode(self.menu_size)
        self.clock = pygame.time.Clock()
        self.screen.fill((0, 0, 0))
        self.bplay = pygbutton.PygButton((55, 140, 75, 35), 'Play !')
        while self.has_to_run:
            pygame.display.update()
            self.clock.tick(30)
            self.screen.fill((0, 0, 0))
            if self.in_game:
                pass
            else:
                self.bplay.draw(self.screen)
                

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.has_to_run = False
                if self.in_game:
                    pass
                else:
                    if 'click' in self.bplay.handleEvent(event):
                        self.in_game = True
                        self.screen = pygame.display.set_mode(self.screen_size)
                        

        

class Client:
    def __init__(self, ip, port):
        self.HOST = ip
        self.PORT = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.HOST, self.PORT))
        
    def send(self, pkt):
        self.socket.send(bytes(pkt, 'utf-8'))
    
    def receive(self):
        return self.socket.recv(1024).decode("utf-8")
    
    def __del__(self):
        self.socket.close()
        
                
if __name__=="__main__":
    client = Interface()
    client.display()
# -




