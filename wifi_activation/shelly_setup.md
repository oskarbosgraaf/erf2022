

##for gen1 devices:


###approach direct device-device connection
*SHELLY HTTP command syntax*
https://[deviceIP]/relay/[channel]?[command]&[command]
or with **authorised** command syntax:
https://[user]:[password]@[deviceIP]/relay/[channel]?[command]&[command]

example: https://gustav:1234321@146.50.60.43/relay/0?turn=on&timer=020
    turn ?plug? with IPaddress 146.50.60.43 on for 20 seconds, as user gustav






###approach MQTT connection protocol
in device settings:
    mqtt_server = brokers address:port (probably dynabically assigned?)
    mqtt_enable = true
if authentication required, set:
    mqtt_user
    mqtt_pass
    maybe(mqtt_max_qos)?
    maybe(mqtt_retain)?
default *MQTTid* is <shellyModel>-<deviceId>
shellyModel is "shellyplug-s" I think?
find <deviceId> in /settings on device

*publishes:*
announce messages@
    shellies/<mqttId>/announce
    announcement is list of attributes{
        id,
        mode (if applicable),
        model,
        mac,
        ip,
        new_fw (true when an update is available),
        fw_ver (contains current firmware version),
    }
availabillity message@
    shellies/<mqttId>/online (with payload true)
complete current state@
    ?device specific?
    reported periodically (default once per 30 seconds)
    possible to set new state message period with@
    /settings with mqtt_update_period
    and disable with value=0


*common MQTT commands*
published@
    shellies/<mqttId>/command for single/specific device, or @
    shellies/command to address all devices subscribed to topic
announce
    """
    will trigger:
    - an announce packet by every Shellu connected to the broker @ shellies/announce and @ shellies/<mqqtId>/announce
    - (since v1.8.0) content of the http /status endpoint @ shellies/<mqttId>/info
    """
update
    """will cause all Shellies to publish their state"""
update_fw
    """perform firmware update (when one is available)"""

*each Shelly model exports its own set of topics for monitoring and control*
all structured under /shellies/<mqttId>

*MQTT topics for shellyplug-s*
shellies/<model>-<deviceid>/relay/0 to report status: on, off or overpower
shellies/<model>-<deviceid>/relay/0/power to report instantaneous power consumption rate in Watts
shellies/<model>-<deviceid>/relay/0/energy to report amount of energy consumed in Watt-minute
shellies/<model>-<deviceid>/relay/0/overpower_value reports the value in Watts, on which an overpower condition is detected
shellies/<model>-<deviceid>/relay/0/command accepts on, off or toggle and applies accordingly
shellies/shellyplug-s-<deviceid>/temperature reports internal device temperature in °C
shellies/shellyplug-s-<deviceid>/temperature_f reports internal device temperature in °F
shellies/shellyplug-s-<deviceid>/overtemperature reports 1 when device has overheated, normally 0


###CHECK SHELLYPLUG-S COLOT COMMUNICATION PROTOCOL STUFF
*ColoT setup*
1. make sure shelly latest firmware (e.g. >v1.10.0)
2. open shelly WebUI with https://<shellyIp> (no clue what shellys IP is gonna be)
3. @ Internet&Security/Advanced-DeveloperSettings enable ColoT
4. enter address of home assistant server at the ColoT peer window (default port si 5683)
5. save and reboot
(6. make device discoverable @Settings/deviceDiscoverable)


###ATTRIBUTES FOR SHELLY PLUG S
@/settings
type=attribute/paramters
- max_power                     int
- led_power_disable             bool
- actions                       hash
- relays                        array of hashes
@/settings/actions
type=action
- btn_on_url
- out_on_url
- out_off_url
@/settings/relay/0
type=attribute/parameters
- name                          string
- appliance_type                string
- ison                          bool
- has_timer                     bool
- overpower                     string
- default_state                 string
- auto_on                       number
- auto_off                      number
- schedule                      bool
- schedule_rules                array of strings
- max_power                     int
- reset                         ??any??
@/status
type=attribute
- relays                        array of hashes
- meters                        array of hashes
- temperature                   int
- overtemperature               int
- tmp.tC                        int
- tmp.tF                        int
- tmo.is_valid                  bool
@/meter/0
type=attribute
- power                         int
- is_valis                      bool
- overpower                     int
- timestamp                     int
- counters                      arrau of ints
- total                         int
@/relay/0
type=attribute
- ison                          bool
- has_timer                     bool
- timer_started                 int
- timer_duration                int
- timer_remaining               int (!experimental!)
- overpower                     bool
- source                        string
type=parameter
- turn                          string -> {"on", "off", "toggle"}
- timer                         number



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

