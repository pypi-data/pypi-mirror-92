from crccheck.crc import Crc32Mpeg2 as CRC32
import remotelab.hal_serial as hw

def _calculate_crc(data):
	crc = CRC32.calc(data).to_bytes(4, byteorder='little')
	return crc

class BBT():
	def __init__(self, dry_run=False):
		self.dry_run = dry_run
		self.pos_x = 0
		self.pos_y = 0
		self.set_x = 0
		self.set_y = 0
		self._id = 0xAC
		self._header = 0x55
		if not self.dry_run:
			self._hw = hw.HWSerial(115200, 0.1)
		self._response_size = 10

	def _construct(self):
		config = self._header.to_bytes(1, 'little') +\
			self._id.to_bytes(1, 'little') +\
			self.set_x.to_bytes(2, 'little') +\
			self.set_y.to_bytes(2, 'little')
		return config + _calculate_crc(config)

	def _parser(self, data):
		if data is not None:
			if bytes(data[-4:]) == _calculate_crc(data[0:self._response_size - 4]):
				if int.from_bytes(bytes(data[1:2]), 'little') == self._id:
					self.pos_x = int.from_bytes(bytes(data[2:4]), 'little')
					self.pos_y = int.from_bytes(bytes(data[4:6]), 'little')

	def set_servo(self, x, y):
		x = int(x)
		y = int(y)
		self.set_x = 500 if x < 500 else 1000 if x > 1000 else x
		self.set_y = 500 if y < 500 else 1000 if y > 1000 else y
		if not self.dry_run:
			self._hw.write(self._construct())
		return

	def get_position(self):
		if not self.dry_run:
			self._parser(self._hw.read(self._response_size))
		return self.pos_x, self.pos_y

class OneDOF():
	def __init__(self, dry_run=False):
		self.dry_run = dry_run
		self.speed = 0
		self.encoder = 0
		self._id = 0xAB
		self._header = 0x55
		self.enable = False
		if not self.dry_run:
			self._hw = hw.HWSerial(115200, 0.1)
		self._response_size = 8

	def _construct(self):
		config = self._header.to_bytes(1, 'little') +\
			self._id.to_bytes(1, 'little') +\
			self.speed.to_bytes(2, 'little')
		return config + _calculate_crc(config)

	def _parser(self, data):
		if data is not None:
			if bytes(data[-4:]) == _calculate_crc(data[0:self._response_size - 4]):
				if int.from_bytes(bytes(data[1:2]), 'little') == self._id:
					self.encoder = int.from_bytes(bytes(data[2:4]), 'little')

	def set_speed(self, value):
		value = int(value)
		value = value if value <= 1000 else 1000
		value = value if value >= 0 else value
		self.speed = (value | (self.enable << 15))
		if not self.dry_run:
			self._hw.write(self._construct())
		return

	def get_encoder(self):
		if not self.dry_run:
			self._parser(self._hw.read(self._response_size))
		return self.encoder

class BB():
	def __init__(self, dry_run=False):
		self.dry_run = dry_run
		self.servo = 0
		self.pos = 0
		self._id = 0xAA
		self._header = 0x55
		if not self.dry_run:
			self._hw = hw.HWSerial(115200, 0.1)
		self._response_size = 8

	def _construct(self):
		config = self._header.to_bytes(1, 'little') +\
			self._id.to_bytes(1, 'little') +\
			self.servo.to_bytes(2, 'little')
		return config + _calculate_crc(config)

	def _parser(self, data):
		if data is not None:
			if bytes(data[-4:]) == _calculate_crc(data[0:self._response_size - 4]):
				if int.from_bytes(bytes(data[1:2]), 'little') == self._id:
					self.pos = int.from_bytes(bytes(data[2:4]), 'little')

	def set_servo(self, value):
		value = 500 if value < 500 else 1000 if value > 1000 else value
		self.servo = int(value)
		if not self.dry_run:
			self._hw.write(self._construct())
		return

	def get_position(self):
		if not self.dry_run:
			self._parser(self._hw.read(self._response_size))
		return self.pos
