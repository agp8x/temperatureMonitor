import onewire, ds18x20
from machine import Pin

ds18_pin = 15

def show_sensors(roms):
	print("\t".join(["raw", "little", "big"]))
	for i, rom in enumerate(roms):
		print(sensor_info(rom))

def sensor_info(rom):
	raw = rom
	little_int = uniq = int.from_bytes(rom, 'little')
	big_int = uniq = int.from_bytes(rom, 'big')
	return str(raw) + "\t" + str(little_int) + "\t" + str(big_int)

def setup():
	ds_pin = Pin(ds18_pin)
	ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
	
	roms = ds_sensor.scan()
	print('Found DS devices: ', roms)
	show_sensors(roms)
	
	return ds_sensor, roms
