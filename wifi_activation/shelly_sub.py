

from paho.mqtt import client as mqtt_client
import warnings
import time


def connect(username: str, broker: str, port: int, token: str = None) -> mqtt_client:
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


def subscribe(client: mqtt_client, topic: str) -> None:
    def on_message(client, userdata, msg):
        print(f"recieved {msg.payload.decode()}\nfrom {msg.topic}\n")

    client.subscribe(topic)
    client.on_message = on_message
    return


def main() -> None:
    username = "gustav_listen"
    token = None
    port = 1883
    broker = "mqtt.eclipseprojects.io"
    topic = "shellies/shellyplug-s<deviceId>/relay/0"

    client = connect(username=username, broker=broker, port=port)
    subscribe(client=client, topic=topic)
    client.loop_forever()


if __name__ == "__main__":
    main()
