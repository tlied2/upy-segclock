import machine

import utime as time
import ujson as json

import mywifi
import mytz

from mymqtt import MyMQTT
from mysensors import MySensor
from ht16k33_seg import Seg7x4
from dummy_display import DummyDisplay

with open('config.json') as configfile:
    CONFIG = json.load(configfile)

# Setup I2C Bus for Display/Sensors
I2C_BUS = machine.I2C(
    scl=machine.Pin(4),
    sda=machine.Pin(5),
    freq=100000)


def init_display():
    ''' Init and return display object '''
    i2cdevs = I2C_BUS.scan()

    print(("I2C Devices Found: {}".format(
        [hex(tmp) for tmp in i2cdevs])))

    if not i2cdevs or len(i2cdevs) > 4:
        print("I2C Bus Error. Might be disconnected, please check connections and pullups.")
        print("Using Dummy Display for debugging")
        return DummyDisplay(enabled=True)

    # Configure Display Object
    disp = Seg7x4(I2C_BUS)
    return disp


def main():

    disp = init_display()
    disp.brightness(CONFIG['clock']['bright'])
    disp.text("88:88")
    disp.show()

    # Init Wifi, RTC, etc
    mywifi.init(CONFIG['wifi'])
    mytz.updatentp(CONFIG['ntp_server'])
    mqttcli = MyMQTT(CONFIG['mqtt'])
    mysensor = MySensor(mqttcli)

    # Loop forever because it crashes otherwise due to Timers it seems
    idx = 0

    mysensor.send_mqtt_data()

    while True:
        try:
            # For offsetting sleep time
            start = time.ticks_ms()

            # Blank display
            disp.fill(0)
            # Write display with current time, offset and formatted as configured
            disp.text(mytz.mkclock(CONFIG['clock']))

            # Must have added this for a reason...
            try:
                disp.show()
            except OSError as tmpex:
                print(("I2C command failed, retrying: %s" % tmpex))
                disp.show()

            # Count our loops
            idx += 1

            # Once a minute send telemetry to MQTT
            if idx % 60 == 0:
                mysensor.send_mqtt_data()

                # Every 10 minutes update our clock from NTP
                if idx % 600 == 0:
                    mytz.updatentp(CONFIG['ntp_server'])
                    # And reset counter as this was our longest delay
                    idx = 0

            # Calculate how long it took to do this loop
            end = time.ticks_ms()
            diff = time.ticks_diff(end, start)

            # And subtract it from our sleep interval, if it was less than 1 second
            # This avoids a negative sleep interval, which should be avoided
            if diff <= 1000:
                time.sleep((1000 - diff) / 1000)

        except KeyboardInterrupt:
            break

        except Exception as ex:
            print(("Encountered error: %s, re-initializing" % ex))
            try:
                disp.text("88:88")
                disp.show()
            except:
                pass
            time.sleep(10)
            machine.reset()


if __name__ == '__main__':
    main()
