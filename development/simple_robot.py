from mirte_robot_lokaal import robot
mirte = robot.createRobot()

# # Import rospy
import rospy
from geometry_msgs.msg import Twist

# Vragen aan Oskar
# 1a We hebben een specifieke distance to the wall nodig. Welke waarden via de sensoren kunnen wij verwachten? 
# 1b Kan je een overzichtje geven hoe dit werkt? Krijgen we afstand in meters uit get_right_distance? 

# 2 Welke functies kunnen we qua sensor input (afstand, IR en camera) nog meer toevoegen?

# 3a Wat denk je van het maken van de bocht en het op juiste afstand blijven van de muur?
# 3b Zou je dat simpel aanpakken of eerder met een AI techniek? Heb je een voorstel?



class RobotMovement:
    def __init__(self, position, velocity):
        self.name = "Gert"
        self.position = position  # example
        self.velocity = velocity  # example
        self.object_detector = None  # CNN_model()  # TODO Francien Sander Derck
        self.cow_counter = None  # Geen idee, zal IR input gebruiken  # TODO Francien Sander Derck
        self.req_distance_to_wall = None
    
    # movement
    def move_forward(self):
        """Move forward until stopped."""
        pass
    
    def move_distance_forward(self, distance):
        """Move forward until distance traveled."""
        pass
    
    def stop_moving(self):
        """Stop moving"""
        pass
    
    # turning
    def turn_90_right(self):
        """Turn 90 degrees to the right"""
        pass
    
    def turn_90_left(self):
        """Turn 90 degrees to the left"""
        pass
    
    def turn_180(self):
        """Turn 180 degrees (turn around)"""
        pass
    
    def turn(self, angle):
        pass
    
    # distance sensors
    def get_front_distance(self):
        """Get distance in front of the robot."""
        pass
    
    def get_right_distance(self):
        """Get distance on the right side of the robot."""
        pass
    
    def get_left_distance(self):
        """Get distance on the left side of the robot."""
        pass
    
    # camera sensors
    def get_camera_stream(self):
        pass
    
    
    # IR sensors TODO Oskar (Wat is de input en output hiervan? Een intensiteitswaarde? Kunnen we Mirte gebruiken?)
    def get_IR_signal(self, input):
        """_summary_

        Args:
            input (_type_): _description_

        Returns:
            _type_: _description_
        """
        pass
    
    # TODOS Francien Sander Derck:
    def check_side_distance(self, side: str, margin: float):
        pass
            
    def check_front_distance(self):
        pass
    
    def adjust_wall_distance(self, distance: float, side: str, margin: float):
        pass
    
    def handle_open_turn(self):
        """When the wall suddenly curves to the right or left, the robot needs to follow the wall.
        Pseudocode:
        1. Keep track of wall distance.
        2. When there is a (great or sudden) change in distance to the wall, walk req_wall_distance to front.
        3. Turn to the side of the wall.
        4. Move forward.
        """
        
        # NOTE: This is not very intelligent, but rather simple. Maybe we can do this more intelligently.
        pass
    
    
    
