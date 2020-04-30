import time

from ble_temperature import setup as setup_ble
from display import setup as setup_display, show
from sensors import setup as setup_sensors


ble_temp = setup_ble()
displays = setup_display()
sensors, roms = setup_sensors()


while True:
	sensors.convert_temp()
	time.sleep_ms(750)	# wait for values
	values = []
	for i, rom in enumerate(roms):
		value = sensors.read_temp(rom)
		print(i, "rom:", rom, "=>", value)
		show(i, displays, value)
		values.append(value)
	ble_temp.set_temperature(*values, notify=True)
	time.sleep(5)
