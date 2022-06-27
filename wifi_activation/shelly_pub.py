

import paho.mqtt.client as mqtt_client
import warnings


class ShellyMQTT():

    def __init__(self, broker:str = None, port: int = None,
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
        self.user               = user
        self.token              = token


    def switchMQTT(self, turn:str = None) -> None:
        """
        Connect to Shelly plug-S over MQTT protocol and switch power
        default turn is 'Toggle'
        """

        if not (self.broker and self.topic):
            raise AttributeMissingError("specify broker and topic to connect via MQTT")
        if not self.token:
            warnings.warn("WARNING: if user or token are not set, MQTT verification might not pass")

        client = mqtt.Client(self.user)

        @client.connect_callback()
        def on_connect(client, userdata, flags, rc):
            print("Connection returned " + str(rc))

        @client.connect_fail_callback()
        def on_connect_fail(client, userdata, flags, rc):
            print("Connection NOT returned ", + str(rc))

        client.connect(self.broker)

        if turn is None:    message = "?turn=toggle"
        elif turn == "on":  message = "?turn=on"
        else:               message = "?turn=off"

        @client.publish_callback()
        def on_publish(client, userdata):
            print(f"published message brih @{rc}")

        #client.on_publish = on_publish
        client.publish(self.topic, message)
        return


    def connectMqtt(self) -> mqtt_client.Client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print(f"connected to shelly broker ({self.broker})")
            else:
                print(f"failed to connect with return code {rc}")

        client = mqtt_client.Client(self.username)

        if self.user_name and self.token:
            client.username_pw_set(self.username, self.token)

        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def publishMqtt(message: str) -> bool:
        #TODO
        pass


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


    mqttBroker ="mqtt.eclipseprojects.io"
    client = mqtt.Client("Temperature_Inside")

    def on_connect():
        print("connection ye")

    client.on_connect = on_connect
    client.connect(mqttBroker)

    def on_publish():
        print("damn, finally a respose")

    client.on_pubish = on_publish
    client.publish("TEMPERATURE", "testing birh")


if __name__ == "__main__":
    main()
