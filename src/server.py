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

BASE_LOCS = [(16, 16),
             (MAP_SIZE[0] - 16, MAP_SIZE[1] - 16),
             (16, MAP_SIZE[1] - 16),
             (MAP_SIZE[0] - 16, 16)]

class Server:
    def __init__(self):
        self.running = False
        self.server_running = True
        self.cli_enabled = True
        self.HOST = "0.0.0.0"
        self.PORT = 50000
        self.clients = []
        self.game_data = DataHandler()
        self.ticks = 0
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
            self.cli()

                       
    def run(self):
        while self.running:
            time.sleep(.01)
            if not (self.ticks % 100):
                self.game_data.opponents.append(Opponent(self.game_data.players))
            for opp_idx in range(len(self.game_data.opponents) - 1, -1, -1):
                opp = self.game_data.opponents[opp_idx]
                if opp.tick():
                    for pl_idx, pl in enumerate(self.game_data.players):
                        if distance(opp.xloc, opp.yloc, pl.xloc, pl.yloc) <= opp.size + pl.size:
                            self.game_data.damage_taken[pl_idx] += opp.damage
                            del self.game_data.opponents[opp_idx]
                else:
                    del self.game_data.opponents[opp_idx]

            self.ticks += 1
        
            
    def run_server(self):
        self.sock = socket.socket()
        self.sock.bind((self.HOST, self.PORT))
        self.sock.settimeout(1)
        self.sock.listen(5)
        while self.server_running:
            try:
                c, addr = self.sock.accept()
                client_idx = len(self.clients)
                self.clients.append(Thread(target=self.client_handler, args=(c, addr, client_idx)))
                self.clients[-1].start()
            except socket.timeout:
                pass
        for clt in self.clients:
            clt.join()
        self.sock.close()
        
        
    def client_handler(self, clientsocket, addr, client_idx):
        if client_idx < len(self.game_data.players):
            self.game_data.players[client_idx].name = clientsocket.recv(BUFFER_SIZE).decode("utf-8")
            self.game_data.indexes[self.game_data.players[client_idx].name] = client_idx
            packet = pickle.dumps(self.game_data)
            clientsocket.send(packet)
            while self.server_running:
                try:
                    tmp_player = pickle.loads(clientsocket.recv(BUFFER_SIZE))
                    self.game_data.players[client_idx] = tmp_player
                    packet = pickle.dumps(self.game_data)
                    clientsocket.send(packet)
                except:
                    break
        clientsocket.close()
                  
            
    def cli(self):
        while True:
            command = input("$:")
            if command == "players":
                print(f"Connected players: {', '.join([pl.name for pl in self.game_data.players if pl.name != 'default'])}")
            if command == "pause" or command == "p":
                if self.running:
                    self.running = False
                    self.runner.join()
                    print("Game has stopped")
                else:
                    print("Game has already stopped")
            if command == "start" or command == "resume" or command == "s" or command == "r":
                if not self.running:
                    self.running = True
                    self.runner = Thread(target=self.run)
                    self.runner.start()
                    print("Game has started")
                else:
                    print("Game has already started")
            if command == "kill" or command == "k":
                if self.running:
                    self.running = False
                    self.runner.join()
                self.server_running = False
                self.server_thread.join()
                sys.exit(0)  


if __name__=="__main__":
    server = Server()
    server.start()
# -




