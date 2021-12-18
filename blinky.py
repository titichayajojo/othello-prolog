from constant import *
from ghost import Ghost

class Blinky(Ghost):
    def __init__(self, position, game, pac):
        super().__init__(position, game, pac)
        self.direction = Vector2(1,0)
        self.in_home = 0

    ''' find grid position of the target '''
    def find_target(self):
        if self.mode != "frighten":
            pac_pos = "node({},{})".format(int(self.pac.grid_position.x), int(self.pac.grid_position.y))
            pac_dir = [int(self.pac.pac_direction[0]),int(self.pac.pac_direction[1])]
            # print("findTarget(blinky,{},{},{},TargetX,TargetY).".format(self.mode,pac_pos,list(self.pac.pac_direction)))
            result = list(self.prolog.query("findTarget(blinky,{},{},{},TargetX,TargetY).".format(self.mode,pac_pos,pac_dir)))[0]
            
            self.target = Vector2(result['TargetX'],result['TargetY'])


    def pac_revive(self, position):
        super().pac_revive(position)
        self.in_home = 0
        self.direction = Vector2(1,0)

    def __str__(self):
        return "Blinky"

from pyswip import Prolog
prolog = Prolog()
prolog.consult('ghost_ai.pl')
result = list(prolog.query("findTarget(blinky,scatter,_,_,X,Y)."))[0]
print(result)