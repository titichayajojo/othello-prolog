from constant import *
from ghost import Ghost

class Inky(Ghost):
    def __init__(self, position, game, pac, blinky):
        super().__init__(position,game,pac)
        self.blink = blinky

    def find_target(self):
        if self.mode != "frighten":
            pac_pos = "node({},{})".format(int(self.pac.grid_position.x), int(self.pac.grid_position.y))
            pac_dir = [int(self.pac.pac_direction[0]),int(self.pac.pac_direction[1])]
            if self.mode == 'chase':
                blinky_pos = "node({},{})".format(int(self.blink.grid_pos.x), int(self.blink.grid_pos.y))
                # print("findTarget(inky,{},{},{},{},TargetX,TargetY).".format(self.mode,pac_pos,pac_dir,blinky_pos))
                result = list(self.prolog.query("findTarget(inky,{},{},{},{},TargetX,TargetY).".format(self.mode,pac_pos,pac_dir,blinky_pos)))[0]
            else:
                # print("findTarget(inky,{},{},{},node(0,0),TargetX,TargetY).".format(self.mode,pac_pos,pac_dir))
                result = list(self.prolog.query("findTarget(inky,{},{},{},node(0,0),TargetX,TargetY).".format(self.mode,pac_pos,pac_dir)))[0]
            # print(result)
            self.target = Vector2(result['TargetX'],result['TargetY'])
        
    

    def __str__(self):
        return "Inky"