import numpy as np
class Arbiter:
    """Opmerking Derck: Er is een term sensor qualification (blz 89). Daar gaat het over het detecteren van disfunctionele sensoren.
    Dat schijnt relevant te zijn voor arbiters.
    """
    def __init__(self, behavior_names, priority_list, distance_front, distance_left, msg):
        self.behavior_names = behavior_names  # get behaviors from scheduler
        self.priority_list = priority_list  # get priorities from scheduler

        self.distance_front = distance_front
        self.distance_left = distance_left

        self.required_walldist = 0.6
        self.object_distance = 0.3

        self.regions_lidar = {
        'right':  min(msg.ranges[213:355]),
        'fright': min(msg.ranges[355:497]),
        'front':  min(msg.ranges[497:639]),
        'fleft':  min(msg.ranges[639:781]),
        'left':   min(msg.ranges[781:923])
        }

    
    def check_wall_left(self):
        # output = is dit aan de hand ja of nee?
        if self.regions_lidar['left'] <= self.required_walldist:
            return True

        return False

    def check_wall_right(self):
        # output = is dit aan de hand ja of nee?
        if self.regions_lidar['right'] <= self.required_walldist:
            return True

        return False
        
    def check_obstacle(self):
        # output = wil je een obstacle ontwijken ja of nee?
        if (self.regions_lidar['front'] < self.object_distance or self.regions_lidar['fright']< self.object_distance) or self.regions_lidar['fleft']< self.object_distance:
            return True

        return False

    def check_if_complete(self):
        # output = wil je terug naar de base ja of nee?
        pass
    
    def check_corridor(self):
        if (self.regions_lidar['left'] + self.regions_lidar['right']) <= 1:
            return True
        
        return False
    
    def getBehavior(control_array):
        for element in reversed(control_array):
            if element != 0:
                return control_array.index(element)
        
    def arbitrate(self):
        control_array = np.zeros(len(self.behavior_names))
        
        #TODO we have another for find wall (not necessary)
        # follow wall behavior
        control_array[0] = self.check_wall_left()
        
        # homing behavior
        control_array[1] = self.check_if_complete()
        
        # corridor behavior
        control_array[2] = self.check_corridor()
        
        # avoid behavior
        control_array[3] = self.check_obstacle()
        
        behavior = self.getBehavior(control_array)
        
        return behavior