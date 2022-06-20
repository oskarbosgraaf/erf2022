import numpy as np
# Current code for the main program




        

            
            
        
        
        
        
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
            

