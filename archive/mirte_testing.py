from mirte_robot import robot
from time import sleep

def main():
   
    R = robot.createRobot()
    
    speed = -50
    start_dist = 200
    stop_dist = 25
    depth_sens = "sens_dist"

    running = True
    set_global_speed(R, speed)
    
    while running:
        
        distance = R.getDistance(depth_sens)
        print(distance)

        if abs(distance) < 20:
            
            set_global_speed(R, 0)
            ##running = False
            print(f"damn bro, we did this shit with distance {distance}")
            turn_left(R, speed, depth_sens, start_dist)

        sleep(.078)


def set_global_speed(obj, speed):
    obj.setMotorSpeed("motor_l", speed)
    obj.setMotorSpeed("motor_r", speed)
    
    return None


def turn_left(obj, speed, depth_sens, start_dist):
    obj.setMotorSpeed("motor_l", -40)
    obj.setMotorSpeed("motor_r", 40)
    
    for _ in range(10):
        if obj.getDistance(depth_sens) < start_dist:
            sleep(1)
        else: set_global_speed(obj, speed)
    
    return None
   
if __name__ == "__main__":
    main()
