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
from player import Player

SEP_CHAR = '&'
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Interface:
    def __init__(self):
        self.in_game = False
        self.has_to_run = True
        self.menu_size = (115, 75)
        self.screen_size = (1366, 768)
        self.buffer = []
        self.step = 50
        self.ip = None
        self.port = None
        self.name = None
        self.current_packet = None
        self.players = [Player("p1", 10, 10), Player("p2", 490, 490)]
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
                    self.name = tmp[1]
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
            self.clock.tick(2)
            self.screen.fill((0, 0, 0))
            if self.in_game:
                candidate_packet = []
                for p in self.players:
                    candidate_packet.extend([p.name, p.xpos, p.ypos, p.atk_cast])
                for ctrl in self.buffer:
                    if ctrl == 0:
                        candidate_packet[4 * self.idx + 2] = max(0,
                                                                  candidate_packet[4 * self.idx + 2] - self.step)
                    elif ctrl == 1:
                        candidate_packet[4 * self.idx + 2] = min(self.screen_size[1],
                                                                  candidate_packet[4 * self.idx + 2] + self.step)
                    elif ctrl == 2:
                        candidate_packet[4 * self.idx + 1] = max(0,
                                                                  candidate_packet[4 * self.idx + 1] - self.step)
                    elif ctrl == 3:
                        candidate_packet[4 * self.idx + 1] = min(self.screen_size[0],
                                                                  candidate_packet[4 * self.idx + 1] + self.step)
                self.buffer = []
                candidate_packet = [*map(str, candidate_packet)]
                candidate_packet = SEP_CHAR.join(candidate_packet)
                self.current_packet = self.client.send(candidate_packet)
                self.update_packet()
                pygame.draw.circle(self.screen, BLUE, (self.players[0].xpos, self.players[0].ypos), 20)
                pygame.draw.circle(self.screen, RED, (self.players[1].xpos, self.players[1].ypos), 20)
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

                else:
                    if 'click' in self.bplay.handleEvent(event):
                        self.in_game = True
                        self.client = Client(self.ip, self.port, len(self.players))
                        self.current_packet = self.client.send(self.name)
                        self.idx = int(self.current_packet[8])
                        self.update_packet()
                        self.screen = pygame.display.set_mode(self.screen_size)
                        
    def update_packet(self):
        self.players[0].name = self.current_packet[0]
        self.players[0].xpos = self.current_packet[1]
        self.players[0].ypos = self.current_packet[2]
        self.players[0].atk_cast = self.current_packet[3]
        self.players[1].name = self.current_packet[4]
        self.players[1].xpos = self.current_packet[5]
        self.players[1].ypos = self.current_packet[6]
        self.players[1].atk_cast = self.current_packet[7]
        

class Client:
    def __init__(self, ip, port, npl):
        self.HOST = ip
        self.PORT = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.HOST, self.PORT))
        self.n_players = npl
        
    def send(self, pkt):
        self.socket.send(bytes(pkt, 'utf-8'))
        npkt = self.socket.recv(1024).decode("utf-8").split(SEP_CHAR)
        for px in range(self.n_players):
            for i in range(1, 4):
                npkt[4 * px + i] = int(npkt[4 * px + i])
        input(npkt)
        return npkt
    
    def __del__(self):
        self.socket.close()
        
                
if __name__=="__main__":
    client = Interface()
    client.display()
# -


