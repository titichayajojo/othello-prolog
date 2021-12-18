from constant import *
from ghost import Ghost

class Clyde(Ghost):
    def __init__(self, position, game, pac):
        super().__init__(position,game,pac)
    def find_target(self):
        if self.mode != "frighten":
            pac_pos = "node({},{})".format(int(self.pac.grid_position.x), int(self.pac.grid_position.y))
            g_node = "node({}, {})".format(int(self.grid_pos.x), int(self.grid_pos.y))
            # print("findTarget(clyde,{},{},{},TargetX,TargetY).".format(self.mode,pac_pos,list(self.pac.pac_direction)))
            result = list(self.prolog.query("findTarget(clyde,{},{},{},TargetX,TargetY).".format(self.mode,g_node,pac_pos)))[0]
            
            self.target = Vector2(result['TargetX'],result['TargetY'])

    def __str__(self):
        return "Clyde"
