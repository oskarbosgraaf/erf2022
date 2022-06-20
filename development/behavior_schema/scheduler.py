from arbiter import Arbiter
from corridorDetection import corridorDetection
from corridorMovement import corridorMovement
from obstacle_avoidance import ObstacleAvoidance
from wall_following import wallFollower
from default_stop import Stop
from homing import Homing


class Scheduler:
    """Every Behavior Based system needs:
    1. A scheduler
    2. A behavior format
    3. A way to specify priority
    4. A connection method
    5. An arbiter
    """
    def __init__(self):
        self.behavior_names = ["find_wall", 'follow_wall', 'homing', 'avoid', 'corridor']  # behaviors
        self.behavior_priority = ["avoid", "corridor", "homing", "follow_wall", "find_wall"]  # initialize priority (descending)
        self.behavior_control = [False for elem in self.behavior_names]  # initialize no behavior wants control --> STOP (alternative for bool is the behavior index) could be initialized in arbiter
        self.sensors = []  # sensor type with index-ID
        self.sensor_data = dict()  # initialize sensor data storage
        self.winner = None  # the winner of arbitration
        self.finished = False  # finished or not
        self.motor_OK = None  # motor status
        self.params = self.initialize_params()  # random params
        self.connected = self.connect_with_host()  # connection with host
        self.initialize_behaviors()  # initialize behavior-instances as attributes
        
    
    def initialize_params(self):
        """Initialize random params.
        Not clear why this could be handy."""
        return None
    
    def connect_with_host(self):
        """There needs to be a connection right?"""
        return None
    
    def read_sensor_data(self):
        return {"data_1" : [], "data_2" : []}
    
    
    def initialize_behaviors(self):
        self.arbiter = Arbiter(self.behavior_names, self.behavior_priority, distance_front, distance_left, msg)
        self.corridor_detector = corridorDetection()
        self.corridor_movement = corridorMovement()
        self.obstacle_avoider = ObstacleAvoidance()
        self.wall_follower = wallFollower()
        self.stop = Stop()  # doesn't really do anything
        self.homing = Homing()  # doesn't really do anything
        return True
        
    def schedule(self):
        """We don't use parallelism, but cooperative multitasking. Each parallel element
        runs for a brief time, then returns control to the scheduler, which then calls the next element.
        
        Functions:
        1. Read sensors
        2. Run behaviors
        3. Arbitrate
        """
        self.finished = False  # when new schedule is started we set finished to be False
        
        # run program
        while not self.finished:
            self.sensor_data = self.read_sensor_data()
            
            # when behaviors show they want control they store this in self.behavior_control
            # we could give this control list as input to arbitrate
            
            # we get the winning behavior (= behavior which wants control with highest priority)
            self.winner = self.arbiter.arbitrate()
            
            # None of them make any sense yet, but I think we want to let the winner run and then go to next iter
            if self.winner == "avoid":
                result = self.obstacle_avoider.avoidObstacle()
            elif self.winner == "corridor":
                result = self.corridor_movement.something()
            elif self.winner == "homing":
                result = self.homing.home()
            elif self.winner == "follow_wall":
                result = self.wall_follower.FollowWall()
            elif self.winner == "find_wall":
                result = self.wall_follower.random_wandering()
            else:
                # else case is currently that there is no winner, so stop case
                result = self.stop()
                self.finished = True
            
            
            # behavior task is executed (execution should take like 1/500 s to 1/10 s)
            # now next iteration is executed until finished
            
        return self
        