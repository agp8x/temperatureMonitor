import onewire, ds18x20, time

from machine import Pin

import tm1637

display_pins = [(14,27), (26,25), (33,32), (23,22)] # (clk, dio)
ds18_pin = 4

def setup(pins=display_pins, val=8888):
	displays = []
	for clk, dio in pinss:
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
	ds_pin = Pin(ds18_pin)
	ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

	roms = ds_sensor.scan()
	print('Found DS devices: ', roms)
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

