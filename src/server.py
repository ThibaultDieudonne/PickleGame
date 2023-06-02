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
import socket
from threading import Thread
from player import Player

SEP_CHAR = '&'
        
class Game:
    def __init__(self):
        self.players = [Player("p1", 10, 10), Player("p2", 490, 490)]
        
    def generate_packet(self):
        dat = []
        for p in self.players:
            dat.extend([p.name, p.xpos, p.ypos, p.atk_cast])
        dat = [*map(str, dat)]
        packet = SEP_CHAR.join(dat)
        return packet
        
    def candidate_packet(self, packet, player_idx):
        dat = packet.split(SEP_CHAR)
        self.players[player_idx].xpos = int(dat[player_idx * 4 + 1])
        self.players[player_idx].ypos = int(dat[player_idx * 4 + 2])
        self.players[player_idx].atk_cast = int(dat[player_idx * 4 + 3])
        
        
class GameHandler:
    def __init__(self):
        self.running = 1
        self.HOST = "127.0.0.1"
        self.PORT = 50000
        self.clients = []
        self.game = Game()
        
    def start(self):
        self.server_thread = Thread(target=self.run_server)
        self.server_thread.start()
        
    def run_server(self):
        self.sock = socket.socket()
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen(5)
        while self.running:
            c, addr = self.sock.accept()
            client_idx = min(len(self.clients), 1) # warning: debug only
            self.clients.append(Thread(target=self.on_new_client, args=(c, addr, client_idx)))
            self.clients[-1].start()
        self.sock.close()
        
    def on_new_client(self, clientsocket, addr, client_idx):
        self.game.players[client_idx].name = clientsocket.recv(1024).decode("utf-8")
        clientsocket.send(bytes(self.game.generate_packet() + SEP_CHAR + str(client_idx), 'utf-8'))
        print (f'{self.game.players[client_idx].name} connected !')
        while True:
            try:
                clientsocket.send(bytes(self.game.generate_packet(), 'utf-8'))
                self.game.candidate_packet(clientsocket.recv(1024).decode("utf-8"), client_idx)
            except:
                break
        clientsocket.close()
        
if __name__=="__main__":
    gh = GameHandler()
    gh.start()
# -


