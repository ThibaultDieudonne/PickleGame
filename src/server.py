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
import pickle
from util import Player, DataHandler, MAP_SIZE

BASE_LOCS = [(16, 16),
             (MAP_SIZE[0] - 16, MAP_SIZE[1] - 16),
             (16, MAP_SIZE[1] - 16),
             (MAP_SIZE[0] - 16, 16)]

class Server:
    def __init__(self):
        self.running = 1
        self.cli_enabled = True
        self.HOST = "0.0.0.0"
        self.PORT = 50000
        self.clients = []
        self.game_data = DataHandler()
        with open('server.cfg', 'rb') as f:
            config = f.readlines()
        for line in config:
            tmp = line.decode("utf-8").replace('\n', '').replace('\r', '').replace(' ', '').split(':')
            if len(tmp) == 2:
                if tmp[0] == "nplayers":
                    for pl in range(int(tmp[1])):
                        self.game_data.players.append(Player("default", BASE_LOCS[pl][0], BASE_LOCS[pl][1]))
        
    def start(self):
        self.server_thread = Thread(target=self.run_server)
        self.server_thread.start()
        if self.cli_enabled:
            self.cli_thread = Thread(target=self.CLI_entry)
            self.cli_thread.start()
        # game events goes here
        
    def CLI_entry(self):
        while True:
            command = input("$:")
            if command == "players":
                print(f"Connected players: {', '.join([pl.name for pl in self.game_data.players if pl.name != 'default'])}")
            
    def run_server(self):
        self.sock = socket.socket()
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen(5)
        while self.running:
            c, addr = self.sock.accept()
            client_idx = min(len(self.clients), 1) # warning: debug only
            self.clients.append(Thread(target=self.client_handler, args=(c, addr, client_idx)))
            self.clients[-1].start()
        self.sock.close()
        
    def client_handler(self, clientsocket, addr, client_idx):
        self.game_data.players[client_idx].name = clientsocket.recv(1024).decode("utf-8")
        self.game_data.indexes[self.game_data.players[client_idx].name] = client_idx
        packet = pickle.dumps(self.game_data)
        clientsocket.send(packet)
        while True:
            try:
                tmp_player = pickle.loads(clientsocket.recv(1024))
                self.game_data.players[client_idx] = tmp_player
                packet = pickle.dumps(self.game_data)
                clientsocket.send(packet)
            except:
                break
        clientsocket.close()
        
        
if __name__=="__main__":
    server = Server()
    server.start()
# -


