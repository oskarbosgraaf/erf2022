
"""
Code for starting camera-based control for the autonomous navigational
robotics hackathon from European Robotics Forum (ERF) 2022, implemented
specifically for the Lely Juno robot.
Team Unuversity of Amsterdam
Github: https://github.com/oskarbosgraaf/erf2022

Written and implemented by:
    Sjoerd Gunneweg
    Thijmen Nijdam
    Jurgen de Heus
    Francien Barkhof
    Oskar Bosgraaf
    Juell Sprott
    Sander van den Bent
    Derck Prinzhoorn

last updated: 1st of July, 2022
"""

import camera
import old # contains previous version of our camera.py file

if __name__ == '__main__':
    print( " === Starting Program === " )
    
    # (un)comment for use of previous version camera-based control
    # cam = old.Camera()
    # cam.video_blob_direction()

    cam = camera.Camera()
    cam.video_blob_direction()


    print("done with main function :)")