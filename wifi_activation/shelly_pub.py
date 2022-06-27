

from paho.mqtt import client as mqtt_client
import warnings


class ShellyMQTT():

    def __init__(self, broker:str = None, port: int = 1883,
                 topic:str = "shellies/shellyplug-s-<deviceId>/relay/0",
                 username:str = "gustav", token:str = None
                 ) -> None:
        """
        TODO:
            add <deviceId> in default topic value for relay of stwitch status
        """
        self.broker             = broker
        self.port               = port
        self.topic              = topic
        self.username           = username
        self.token              = token
        self.client             = None

    def switchMQTT(self, turn:str = None) -> None:
        """
        Connect to Shelly plug-S over MQTT protocol and switch power
        default turn is 'Toggle'
        """

        if not (self.broker and self.topic):
            raise AttributeMissingError("specify broker and topic to connect via MQTT")
        if not self.token:
            warnings.warn("WARNING: if user or token are not set, MQTT verification might not pass")

        self.client = mqtt.Client(self.user)

        @client.connect_callback()
        def on_connect(client, userdata, flags, rc):
            print("Connection returned " + str(rc))

        @client.connect_fail_callback()
        def on_connect_fail(client, userdata, flags, rc):
            print("Connection NOT returned ", + str(rc))

        self.client.connect(self.broker)

        if turn is None:    message = "?turn=toggle"
        elif turn == "on":  message = "?turn=on"
        else:               message = "?turn=off"

        @client.publish_callback()
        def on_publish(client, userdata):
            print(f"published message brih @{rc}")

        #client.on_publish = on_publish
        self.client.publish(self.topic, message)
        return


    def connectMqtt(self) -> None:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print(f"connected to shelly broker ({self.broker})")
            else:
                print(f"failed to connect with return code {rc}")

        self.client = mqtt_client.Client(self.username)

        if self.username and self.token:
            self.client.username_pw_set(self.username, self.token)

        self.client.on_connect = on_connect
        self.client.connect(self.broker, self.port)
        return

    def publishMqtt(msg: str) -> None:
        self.client.publish(topic, msg)
        if result[0] == 0:
            print(f"message successfully published to {self.topic}")
        else: print(f"failed to publish message to {self.topic}")
        return


def main():
    """
    in AP mode:
        HTTP server on port 80
        IP -> 192.168.33.1/
    announce HTTP service on port 80 via mDNS
        hostname in the form of:
            shelly<model>-XXXXXXXXXXXX
    """
    #connection = ShellyMQTT(broker="mqtt.eclipseprojects.io", topic="TEST", user="gustav")
    #connection.switchMQTT(turn="on")


    broker ="mqtt.eclipseprojects.io"
    port = 1833
    shelly = ShellyMQTT(broker=broker, port=port)
    shelly.connectMqtt()
    for i in range(30):
        shelly.publishMqtt(msg=f"{i}th message")
        time.sleep(3)
    exit(0)


if __name__ == "__main__":
    main()



