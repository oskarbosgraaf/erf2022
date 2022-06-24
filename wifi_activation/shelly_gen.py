
import paho.mqtt.client as mqtt
import time
from dataclasses import dataclass
from typing import Optional

"""
first template to establish MQTT connection
and start publishing on a specific topic

prerequisite packages:
    mosquitto
prerequisite libraries:
    paho-mqtt

by Oskar Gustav Bosgraaf
"""

class Block:
    """
    Holds all data needed for successfull MQTT connection and publishing
    """
    def __init__(self,
                 user: Optional[str] = None,
                 broker: Optional[str] = None,
                 topic: Optional[str] = None,
                 token: Optional[str] = None):
        self.user = client
        self.broker = broker
        self.topic = topic
        self.token = token
        self._subscription = False


    def __repr__(self):
        tmp1 = f"dataBlock {self} for MQTT connection establishment\n"
        tmp2 = f"----------------------\nuser {self.user}\n"
        tmp3 = f"broker {self.broker}\ntopic {self.topic}\n"
        tmp4 = f"token {self.token}\n----------------------\n"
        tmp5 = f"current subscription status: {self._subscription}\n"
        return tmp1 + tmp2 + tmp3 + tmp4 + tmp5


def shellyConnect(block): -> Optional[mqtt.Client]
    client = mqtt.Clinet("block.user")
    try: client.connect(block.broker)
    except: raise ConnectionError("could not connect to broker")
    return client

def shellyPublish(block, package):
    pass



def main():
    shellBlock = Block(user="Gustav",
                        broker="mqtt.eclipseprojects.io",
                        topic="relay")
    client = shellyConnect(shellBlock)




if __name__ == "__main__":
    main()
