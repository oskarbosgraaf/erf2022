"""
MQTT and HTTP publishing for shelly plug-s
needed dependencies:
    pip3 install paho-mqtt
    pip3 install requests
by Oskar Bosgraaf
oskar.bosgraaf@gmail.com
"""

from paho.mqtt import client as mqtt_client
import requests
import warnings
import time

def connect(username: str, broker: str, port: int = 1883,
            token: str = None) -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"connected to shelly broker")
        else:
            print(f"failed to connect with return code {rc}")

    client = mqtt_client.Client(username)
    if not (username and token):
        client.username_pw_set(username, token)

    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client: mqtt_client, topic: str, turn: str = None) -> None:
    if turn == None:    msg = "?turn=toggle"
    elif turn == "on":  msg = "?turn=on"
    elif turn -- "off": msg = "?turn=off"
    else: raise PlugError("you need to specify a turn value ('on', 'off') or 'None' for toggle")

    result = client.publish(topic, msg)
    if result[0] == 0:
        print(f"sent '{msg}'\n to topic '{topic}'")
    else: print(f"failed to send message to topic {topic}")
    return


def loginHTTP(deviceIp: str = "192.168.33.1", deviceId: str = None,
              model: str = "shellyplug-s", username: str = "gustav",
              token: str = None) -> None:
    raise notImplementedError("ga doen dan\nof is het uberhaupt wel benodigd?")


def switchBasicHTTP(deviceIp: str = "192.168.33.1", deviceId: str = None,
               model: str = "shellyplug-s", username: str = "gustav",
               password: str = None, turn: str = "off") -> None:
    url = "https://" + deviceIp + "/settings/relay?turn=" + turn
    r = requests.get(url, auth=(username, password))
    print(r.status_code)
    print()
    print(r.json())
    print("--------------------------------------------------------------------")


def switchBasicHTTP(deviceIp: str = "192.168.33.1", deviceId: str = None,
                    model: str = "shellyplug-s", token: str = None,
                    turn: str = "off") -> None:
    url = "https://" + deviceIp + "/settings/relay?turn=" + turn
    header = {"Authorization" : f"Basic {token}"}
    r = requests.get(url, headers=header)
    print(r.status_code)
    print()
    print(r.json())
    print("--------------------------------------------------------------------")


def getBasicSettingsHTTP(deviceIp: str = "192.168.33.1",
                         model: str = "shellyplug-s") -> None:
    url = "https://" + str(deviceIp) + "/shelly"
    r = requests.get(url)
    print(r.text)
    print()
    print(r.json())
    print("--------------------------------------------------------------------")
    return


def testMQTT() -> None:
    client = connect(username="gustav",
                     broker="mqtt.eclipseprojects.io",
                     port=1883)
    for i in range(30):
        print(f"publishing message #{i}")
        publish(client, "shellies/shellyplug-s<deviceId>/relay/0", turn=None)
        time.sleep(3)
    return


def testHTTP() -> None:
    print("basic settings:")
    getBasicSettingsHTTP()



def main():
    """
    in AP mode:
        HTTP server on port 80
        IP -> 192.168.33.1/
    announce HTTP service on port 80 via mDNS
        hostname in the form of:
            shelly<model>-XXXXXXXXXXXX
    """
    # testMQTT()
    testHTTP()


if __name__ == "__main__":
    main()



