from mirte_robot import robot
from time import sleep

R = robot.createRobot()

# return distance of depth sensor
def check_distance(depth_sens):
    distance = R.getDistance(depth_sens)

    return distance

# set speed of both motors
def go_straight(speed):
    R.setMotorSpeed("motor_l", speed)
    R.setMotorSpeed("motor_r", speed)
    
    return None

# let right motor go faster for a certain duration
def adjust_left(duration, speed):
    
    do = True
    while do:
        R.setMotorSpeed("motor_l", speed)
        R.setMotorSpeed("motor_r", speed + 5)

        sleep(duration)

    go_straight(speed)

    return None

def adjust_right(duration, speed):

    do = True
    while do:
        R.setMotorSpeed("motor_l", speed + 5)
        R.setMotorSpeed("motor_r", speed)

        sleep(duration)

    go_straight(speed)

    return None

def turn_right(duration, speed):
    
    do = True

    while do:
        R.setMotorSpeed("motor_l", 40)
        R.setMotorSpeed("motor_r", -40)

        sleep(duration)

    go_straight(speed)

    return None

# move alongside wall (only straight)
def main():
    # init speed
    speed = 50

    # duration of adjustment
    duration_adj = 1
    duration_turn = 2

    # distance in front
    stop_dist = 25
    
    # desired distance to wall
    min_dist = 20
    max_dist = 30

    # senors
    depth_sens_left = "sens_dist_left"
    depth_sens_front = "sens_dist_front"

    # IF FLAG: FOLLOW_WALL is True
    while True:
        distance_wall = check_distance(depth_sens_left)
        distance_front = check_distance(depth_sens_front)

        if distance_front > stop_dist:
            go_straight(0)
            turn_right(duration_turn)
            
            
        if (min_dist < distance_wall) & (distance_wall < max_dist):
            go_straight(50)
        
        if (distance_wall < min_dist):
            adjust_right(duration_adj, speed)

        if (distance_wall > max_dist):
            adjust_right(duration_adj, speed)


