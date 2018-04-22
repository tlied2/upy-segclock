# upy-segclock
NTP clock with Adafruit 1.2" I2C display on ESP8266 in Micropython

This project uses submodules. Clone with `git clone --recurse-submodules` or `git submodule init` in each submodule directory.

## BOM
- 1x esp8266 development board with USB - I used a nodemcuv2 variant
- 1x Adafruit 1.2" 4-Digit 7-Segment Display with I2C Backpack - there are a few color choices. Based on HT16K33 controller.
- 1x DHT-22 Temperature and Humidity Sensor
- 3x 10K resistors for pullups
- 1x old phone USB charger - to power it when it is on the wall

## Wiring
Pins are currently hardcoded

### Adafruit I2C Backpack
1. IO &rarr; 3V3
2. \+ &rarr; VIN (5V)
3. \- &rarr; GND
4. D &rarr; D1 (Pin 5) + pullup resistor to IO or 3V3
5. C &rarr; D2 (Pin 4) + pullup resistor to IO or 3V3

### DHT22
1. VDD &rarr; 3V3 
2. Data &rarr; D5 (Pin 14) + pullup resistor to VDD or 3V3
3. NC
4. GND &rarr; GND

## Getting Started
- Install micropython to your board https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html
- `cp config.json.example config.json` and edit config.json to match your environment
- Upload the sources to the device - load.sh is an example using [ampy](https://github.com/adafruit/ampy) to load them over serial

## TODO
- Configurable I/O Pins
- Improve MQTT configurability
- Improve DHT-22 configurability
- Make DHT-22 optional
- Improve localization (Timezone and DST offsetting)
