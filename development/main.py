import numpy as np
# Current code for the main program

class Arbiter:
    def __init__(self, lidar, distance_front, distance_left):
        self.behavior_names = ['find wall', 'follow wall', 'homing', 'avoid', 'corridor']
        self.lidar = lidar
        self.distance_front = distance_front
        self.distance_left = distance_left
        
    def check_find_wall(self):
        # output is dus false als er iets in de buurt is
        # en anders true
        pass
    
    def check_wall_left(self):
        # output = is dit aan de hand ja of nee?
        pass

    def check_wall_right(self):
        # output = is dit aan de hand ja of nee?
        pass
        
    def check_obstacle(self):
        # output = wil je een obstacle ontwijken ja of nee?
        pass
        
    def check_if_complete(self):
        # output = wil je terug naar de base ja of nee?
        pass
    
    def check_corridor(self):
        if self.check_wall_left() and self.check_wall_right():
            return True
        
        return False
    
    def getBehavior(control_array):
        for element in reversed(control_array):
            if element != 0:
                return control_array.index(element)
        
    def arbitrate(self):
        control_array = np.zeros(len(self.behavior_names))
        
        # find wall behavior
        control_array[0] = self.check_wall_left()
        
        # follow wall behavior
        control_array[1] = self.check_find_wall()
        
        # homing behavior
        control_array[2] = self.check_wall_left()
        
        # corridor behavior
        control_array[3] = self.check_wall_left()
        
        # avoid behaviour
        control_array[4] = self.check_wall_left()
        
        behavior = self.getBehavior(control_array)
        
        return behavior

        

            
            
        
        
        
        
def detect_juno():
    # if juno is within certain range
    if seen:
        return True
    
    
    return False

# switch diretion of both Junos
def switch():
    return None

def find_wall():
    pass

def avoid_object():
    pass

def move_through_corridor():
    pass

def follow_wall():
    pass
# check 
def check_surrounding():
    if nothing_close:
        return 'nothing close'
    if object:
        return 'object'
    if corridor:
        return 'corridor'
    if wall:
        return 'wall'
    
while True:
    J = detect_juno()
    
    if J:
        switch()
        
    else:
        surrounding = check_surrounding()
        
        if surrounding == 'nothing close':
            find_wall()
            
        elif surrounding == 'object':
            avoid_object()
            
        elif surrounding == 'corridor':
            move_through_corridor()
        
        else:
            follow_wall()
            

