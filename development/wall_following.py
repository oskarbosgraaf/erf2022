class WallFollowingLogic:
    def __init__(self, wall_side, left: bool, right: bool, front: bool):
        self.wall_side = wall_side
        self.left_wall = left  # is there something close or not?
        self.right_wall = right  # is there something close or not?
        self.front_wall = front  # is there something close or not?
        
    def forward(self):
        pass
    
    def turn_right(self):
        pass
    
    def turn_left(self):
        pass
    
    def choose_move(self):
        if self.wall_side == "left":
            # drive along wall
            if self.left_wall and not self.front_wall:
                self.forward()
                
            # corner to the right
            elif self.left_wall and self.front_wall:
                self.turn_right()
                
            # open curved corner to the left (keep wall left)
            elif not self.left_wall and not self.front_wall:
                self.turn_left()
            
            # get back to the wall and keep the wall left
            elif not self.left_wall and self.front_wall:
                self.turn_right()
            
        elif self.wall_side == "right":
            # drive along wall
            if self.right_wall and not self.front_wall:
                self.forward()
            
            # corner to the left
            elif self.right_wall and self.front_wall:
                self.turn_left()
                
            # open curved corner to the right (keep wall right)
            elif not self.right_wall and not self.front_wall:
                self.turn_right()
                
            # get back to the wall and keep the wall right
            elif not self.right_wall and self.front_wall:
                self.turn_left()



