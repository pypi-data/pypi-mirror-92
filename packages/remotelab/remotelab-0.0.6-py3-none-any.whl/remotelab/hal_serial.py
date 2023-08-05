import serial
import time

class HWSerial():
	def __init__(self, baudrate, timeout):
		self.baudrate = baudrate
		self.timeout = timeout
		self._interpacket_delay = 10/self.baudrate * 1000000000 #convert to nanoseconds
		self._serial = serial.Serial(port = '/dev/serial0', baudrate = self.baudrate, timeout = self.timeout)
		self._last_invoked = time.monotonic_ns()

	def write(self, data):
		#Make sure program waits enough between packages. Crucial for target hardware.
		t = time.monotonic_ns()
		period = self._interpacket_delay - (t - self._last_invoked)
		self._last_invoked = t
		period = period if period > 0 else 0
		time.sleep(period)
		self._serial.write(bytes(data))

	def read(self, expected):
		if self._serial.inWaiting() >= expected:
			return bytearray(self._serial.read(expected))
