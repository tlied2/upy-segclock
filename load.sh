#!/bin/sh

PORT="/dev/ttyUSB0"

FILES="\
config.json \
dummy_display.py \
main.py \
mysensors.py \
mytz.py \
upy-mylib/mywifi.py \
upy-mylib/mymqtt.py \
micropython-adafruit-ht16k33/ht16k33_matrix.py \
micropython-adafruit-ht16k33/ht16k33_seg.py \
"

for FILE in $FILES; do
echo ampy -p $PORT put $FILE ;
ampy -p $PORT put $FILE ;
done
