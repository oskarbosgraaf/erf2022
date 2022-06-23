

##for gen1 devices:
in device settings:
    mqtt_server = brokers address:port (probably dynabically assigned?)
    mqtt_enable = true
if authentication required, set:
    mqtt_user
    mqtt_pass
    maybe(mqtt_max_qos)?
    maybe(mqtt_retain)?
default *MQTTid* is <shellyModel>-<deviceId>
shellyModel is "shellyPlugS" I think?
find <deviceId> in /settings on device

*publishes:*
announce messages@
    shellies/announce
    or since v1.6.0, announce messages@
    shellies/<mqttId>/announce






?? for gen2 devices?
**check shelly MQTT connection:**
    export SHELLY=<deviceIPaddress>
    curl -X POST -d '{"id":1, "method":"Mqtt.GetStatus"}' http://#{SHELLY}rpc
    *should return 'true' if MQTT connection is acctive*

**check configuration**
    curl -X POST -d '{"id":1, "method":"Mqtt.GetConfig"}' http://${SHELLY}/rpc

**if either connection or config are false: set new MQTT connection**
    curl -X POST -d '{"id":1, "method":"Mqtt.SetConfig", "params":{"config":{"enable":true, "server":"broker.hivemq.com:1883"}}}' http://${SHELLY}/rpc
    curl -X POST -d '{"id":1, "method":"Shelly.Reboot"}' http://${SHELLY}/rpc
    *then check connecction status again*
    curl -X POST -d '{"id":1, "method":"Mqtt.GetStatus"}' http://#{SHELLY}rpc 

**subscribe to MQTT notifications**
    export MQTT_SERVER="broker.hivemq.com"
    export MQTT_PORT=1883
    export SHELLY_ID="shellypro4pm-f008d1d8b8b8" # The <shelly-id> of your device
    *for notifications:*
    mosquitto_sub -h ${MQTT_SERVER} -p ${MQTT_PORT} -t ${SHELLY_ID}/events/rpc
    *for messages on connection - disconnection*
    mosquitto_sub -h ${MQTT_SERVER} -p ${MQTT_PORT} -t ${SHELLY_ID}/online

