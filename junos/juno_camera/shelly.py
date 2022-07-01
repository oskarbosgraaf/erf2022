
"""
Code for Shelly Plug-S operation for the autonomous navigational robotics
hackathon from European Robotics Forum (ERF) 2022, implemented specifically for
the Lely Juno robot.
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

import time
import requests

def switchPlug(toggle: str = None) -> None:
    """
    Send unauthorised GET request to both
    Shelly Plug-S's to toggle power state
    """
    url1 = "http://192.168.11.190/relay/0?turn="
    url2 = "http://192.168.11.191/relay/0?turn="
    if toggle is None:
        url1 += "toggle"
        url2 += "toggle"
    elif toggle == "off":
        url1 += "off"
        url2 += "off"
    elif toggle == "on":
        url1 += "on"
        url2 += "on"

    r1 = requests.get(url1)
    r2 = requests.get(url2)
    return


def main():
    switchPlug()

if __name__ == "__main__":
    main()
