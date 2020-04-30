# This example demonstrates a simple temperature sensor peripheral.
#
# The sensor's local value updates every second, and it will notify
# any connected central every 10 seconds.

import bluetooth
import random
import struct
import time
from ble_advertising import advertising_payload

from micropython import const
_IRQ_CENTRAL_CONNECT                 = const(1 << 0)
_IRQ_CENTRAL_DISCONNECT              = const(1 << 1)

# org.bluetooth.service.environmental_sensing
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)

_UUIDS = (
	bluetooth.UUID(0x2A6E),	# org.bluetooth.characteristic.temperature ()
	bluetooth.UUID(0x2A3C),	# "Scientific Temperature Celsius"
	bluetooth.UUID(0x2A1F),	# "Temperature Celsius"
	bluetooth.UUID(0x2A1E),	# "Intermediate Temperature"
	bluetooth.UUID(0x2A1C),	# "Temperature Measurement"
)


_ENV_SENSE_SERVICE = (_ENV_SENSE_UUID, [(uuid, bluetooth.FLAG_READ|bluetooth.FLAG_NOTIFY,) for uuid in _UUIDS],)

# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_THERMOMETER = const(768)

class BLETemperature:
    def __init__(self, ble, name='mpy-temp'):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(handler=self._irq)
        (self._handles,) = self._ble.gatts_register_services((_ENV_SENSE_SERVICE,))
        self._connections = set()
        self._payload = advertising_payload(name=name, services=[_ENV_SENSE_UUID], appearance=_ADV_APPEARANCE_GENERIC_THERMOMETER)
        self._advertise()

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _, = data
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _, = data
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()

    def set_temperature(self, temperatures, notify=False):
        # Data is sint16 in degrees Celsius with a resolution of 0.01 degrees Celsius.
        # Write the local value, ready for a central to read.
        if not len(list(self._handles)) == len(temperatures):
        	print("ERROR -- uneven length of handles and temperatures", len(list(self._handles)), len(temperatures), "|", list(self._handles),":", temperatures)
        	return
        for i, handle in enumerate(self._handles):
        	self._ble.gatts_write(handle, struct.pack('<h', int(temperatures[i] * 100)))
        if notify:
            for conn_handle in self._connections:
                # Notify connected centrals to issue a read.
                for handle in self._handles:
                	self._ble.gatts_notify(conn_handle, handle)

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)


def demo():
    ble = bluetooth.BLE()
    temp = BLETemperature(ble)

    t = 25
    i = 0

    while True:
        # Write every second, notify every 10 seconds.
        i = (i + 1) % 10
        temp.set_temperature(t, t/2, notify=i == 0)
        # Random walk the temperature.
        t += random.uniform(-0.5, 0.5)
        time.sleep_ms(1000)

def setup():
    ble = bluetooth.BLE()
    temp = BLETemperature(ble)
    return temp

if __name__ == '__main__':
    demo()

