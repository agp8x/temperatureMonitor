import time

from machine import Pin

import tm1637
import sensors

display_pins = [(14,27), (26,25), (33,32), (23,22), (19,21)] # (clk, dio)

def setup(pins=display_pins, val=8888):
	displays = []
	for clk, dio in pins:
		print(clk, dio)
		tm = tm1637.TM1637(clk=Pin(clk), dio=Pin(dio))
		tm.number(val)
		displays.append(tm)
	return displays

def off(displays):
	for tm in displays:
		tm.show("    ")

def show(i, displays, value):
	if i < len(displays):
		displays[i].number(int(value))

def run():
	ds_sensor, roms = sensors.setup()
	
	displays = setup()

	while True:
		ds_sensor.convert_temp()
		time.sleep_ms(750)
		for i, rom in enumerate(roms):
			value = ds_sensor.read_temp(rom)
			print(rom)
			print(value)
			show(i, displays, value)
		time.sleep(5)

