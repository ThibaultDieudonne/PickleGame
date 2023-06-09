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
from util import *
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygbutton


TICK_RATE = 60
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLORS = (BLUE, GREEN, YELLOW, PURPLE)


class Client:
    def __init__(self):
        self.in_game = False
        self.has_to_run = True
        self.menu_size = (115, 75)
        self.screen_size = MAP_SIZE
        self.buffer = []
        self.ip = None
        self.port = None
        self.name = None
        self.socket = None
        self.gs = None
        with open('../player.cfg', 'rb') as f:
            config = f.readlines()
        for line in config:
            tmp = line.decode("utf-8").replace('\n', '').replace('\r', '').replace(' ', '')
            if "#" in tmp:
                tmp = tmp.split("#")[0]
            tmp = tmp.split(':')
            if len(tmp) == 2:
                if tmp[0] == "ip":
                    self.ip = tmp[1]
                elif tmp[0] == "port":
                    self.port = int(tmp[1])
                elif tmp[0] == "name":
                    self.name = tmp[1] + "#" + str(random.randint(1000, 9999))
        if self.ip is None or self.port is None or self.name is None:
            raise Exception("Missing ip, port or name in game.cfg")
        # else:
        #     print(f'[{self.name}@{self.ip}:{self.port}]')
                       
    def display(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Pickle Game")
        self.font = pygame.font.SysFont('Berlin Sans FB', 15)
        self.screen = pygame.display.set_mode(self.menu_size)
        self.clock = pygame.time.Clock()
        self.screen.fill(BLACK)
        self.bplay = pygbutton.PygButton((20, 20, 75, 35), 'Play !')
        
        while self.has_to_run:
            pygame.display.update()
            self.clock.tick(TICK_RATE)
            self.screen.fill(BLACK)
            if self.in_game:
                player = self.gs.players[self.gs.indexes[self.name]]
                cq = ClientQuery(self.gs.players[self.gs.indexes[self.name]])
                if player.active:
                    for ctrl in self.buffer:
                        if ctrl == 0:
                            cq.yloc = max(0, cq.yloc - player.speed)
                        elif ctrl == 1:
                            cq.yloc = min(self.screen_size[1], cq.yloc + player.speed)
                        elif ctrl == 2:
                            cq.xloc = max(0, cq.xloc - player.speed)
                        elif ctrl == 3:
                            cq.xloc = min(self.screen_size[0], cq.xloc + player.speed)
                else:
                    self.screen.blit(self.font.render("GAME OVER", False, WHITE), (MAP_SIZE[0] - 100, 2))
                self.send_and_update(cq)
                for pl_idx, pl in enumerate(self.gs.players):
                    pygame.draw.circle(self.screen, PLAYER_COLORS[pl_idx], (pl.xloc, pl.yloc), pl.size)
                for opponent in self.gs.opponents:
                    pygame.draw.circle(self.screen, RED, (opponent.xloc, opponent.yloc), opponent.size)
                self.screen.blit(self.font.render("Damage taken", False, WHITE), (2, 2))
                for pl_idx, pl in enumerate(self.gs.players):
                    self.screen.blit(self.font.render(f"{pl.name}: {self.gs.players[pl_idx].damage_taken}", False, WHITE), (2, 22 + 20 * pl_idx))
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
        try:
            if isinstance(packet, str):
                packet = bytes(packet, "utf-8")
            else:
                packet = pickle.dumps(packet)
            self.socket.send(packet) 
            self.gs = pickle.loads(self.socket.recv(BUFFER_SIZE))
        except Exception as e:
            sys.exit(0)

    
    def __del__(self):
        if self.socket is not None:
            self.socket.close()
        
                
if __name__=="__main__":
    client = Client()
    client.display()
# -


