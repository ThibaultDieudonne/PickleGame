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
from player import Player, SEP_CHAR
        
class Server:
    def __init__(self):
        self.running = 1
        self.HOST = "0.0.0.0"
        self.PORT = 50000
        self.clients = []
        self.players = [Player("p1", 10, 10), Player("p2", 490, 490)]
        
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
        self.players[client_idx].name = clientsocket.recv(1024).decode("utf-8")
        clientsocket.send(bytes(self.generate_packet() + SEP_CHAR + str(client_idx), 'utf-8'))
        print (f'{self.players[client_idx].name} connected !')
        while True:
            try:
                self.players[client_idx].update(clientsocket.recv(1024).decode("utf-8"))
                clientsocket.send(bytes(self.generate_packet(), 'utf-8'))
            except:
                break
        clientsocket.close()
        
    def generate_packet(self):
        dat = []
        for p in self.players:
            dat.extend([p.name, p.xpos, p.ypos, p.atk_cast])
        dat = [*map(str, dat)]
        packet = SEP_CHAR.join(dat)
        return packet
        
if __name__=="__main__":
    server = Server()
    server.start()
# -


