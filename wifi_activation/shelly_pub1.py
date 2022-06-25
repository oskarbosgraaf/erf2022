


import paho.mqtt.client as mqtt
import time

def main():
    mqttBroker  = "mqtt.eclipseprojects.io"
    mqttUser    = "gustav"
    mqttPassw   = None
    mqttTopic   = "hella_testing"

    message     = "test_mqtt"

    client = mqtt.Client(mqttUser)
    client.connect(mqttBroker)

    for i in range(100):
        client.publish(mqttTopic, f"{message} number {i}")
        print(f"published '{message} number {i}' in topic {mqttTopic}")
        time.sleep(2)

if __name__ == "__main__":
    main()
