
from pyShelly import pyShelly
from typing import Optional
from urllib import request
import time as time

"""
for use of this code we need:
sudo apt update && pip3 install zeroconf websocket-client && pip3 install pyShelly

1. get BLOCK
2. get device(BLOCK)
3.?get connection
4. send MQTT / HTTP commands
5. drink a biertje
"""

def shellyInfo(shelly):
    print(f"info shelly {shelly} in version {shelly.version()}")
    print(f"--------------------")
    print(f"MDNS? {shelly.mdns_enabled}")
    print(f"blocks: {shelly.blocks}")
    print(f"devices: {shelly.devices}")
    print(f"usename: {shelly.username}")
    print(f"password: {shelly.password}")
    print(f"--------------------")



def device_added(dev, code):
    print (dev," ",code)

def shellyConnection(dev:str, code:str):
    shelly = pyShelly()
    shellyInfo(shelly)
    shelly.cb_device_added.append(device_added)
    print(shelly.cb_device_added)
    shelly.start()
    shelly.discover()
    print("discovering avialable devices")
    time.sleep(5)

    shelly.check_by_ip()
    shellyInfo(shelly)

    return shelly

def main():
    dev = "SHPLG-S"

    shelly = shellyConnection(dev)

    shelly.close()

if __name__ == "__main__":
    main()

