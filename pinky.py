from constant import *
from ghost import Ghost

class Pinky(Ghost):
    def __init__(self, position, game, pac):
        super().__init__(position,game,pac)
    def find_target(self):
        if self.mode != "frighten":
            pac_pos = "node({},{})".format(int(self.pac.grid_position.x), int(self.pac.grid_position.y))
            pac_dir = [int(self.pac.pac_direction[0]),int(self.pac.pac_direction[1])]
            # print("findTarget(pinky,{},{},{},TargetX,TargetY).".format(self.mode,pac_pos,list(self.pac.pac_direction)))
            result = list(self.prolog.query("findTarget(pinky,{},{},{},TargetX,TargetY).".format(self.mode,pac_pos,pac_dir)))[0]
            self.target = Vector2(result['TargetX'],result['TargetY'])


    def __str__(self):
        return "Pinky"