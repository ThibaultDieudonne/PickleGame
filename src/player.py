SEP_CHAR = '&'

class Player:
    def __init__(self, name, xpos=0, ypos=0, atk_cast=0):
        self.name = name
        self.xpos = xpos
        self.ypos = ypos
        self.atk_cast = 0

    def args_count(self):
        return len(vars(self))
    
    def clone(self):
        return Player(self.name, self.xpos, self.ypos, self.atk_cast)
    
    def packet(self):
        vrs = vars(self)
        return SEP_CHAR.join([str(vrs[v])for v in vrs])
    
    def update(self, packet):
        dat = packet.split(SEP_CHAR)
        self.xpos = int(dat[1])
        self.ypos = int(dat[2])
        self.atk_cast = int(dat[3])