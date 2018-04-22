import esp
import dht
import machine
import network
import utime as time
import ujson as json
import mytz


class MySensor(object):

    def __init__(self, mqttcli):
        self.mqttcli = mqttcli
        self.sensor = dht.DHT22(machine.Pin(14))

    def send_mqtt_data(self):
        ''' Collects all sensors, and sends MQTT packets for each '''

        try:
            self.sensor.measure()
        except OSError as tmpex:
            print(("Unable to read DHT22 sensor: {}".format(tmpex)))

        data = {
            'ipaddr': network.WLAN(network.STA_IF).ifconfig()[0],
            'freemem': esp.freemem(),
            #'voltage': machine.ADC(1).read(),
            'timestamp': time.time(),
            'time': mytz.mktime()
        }

        sensor = {
            'temp': "{0:0.2f}".format(self.sensor.temperature()),
            'humidity': "{0:0.2f}".format(self.sensor.humidity())
        }

        self.mqttcli.pub(b"segclock/system", json.dumps(data))
        self.mqttcli.pub(b"segclock/sensor", json.dumps(sensor))

        return
