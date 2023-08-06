from machine import Pin


import dht 
import time 





class Main:
	"""docstring for ClassName"""
	def __init__(self, pin= None, type = 11):

		self.pin = pin 
		self.is_output = True 
		self.is_input = False
		self.type = type 



	def measure_data(self):
		sensor_pin = Pin(self.pin, Pin.IN, Pin.PULL_UP)

		if self.type==11:

			
			
			sensor = dht.DHT11(sensor_pin)
			time.sleep(5)
			sensor.measure()
			return {'temperature':sensor.temperature(), 'humidity': sensor.humidity()}

		else:

			sensor = dht.DHT22(sensor_pin)
			time.sleep(5)
			sensor.measure()
			return {'temperature':sensor.temperature(), 'humidity': sensor.humidity()}


	def input(self):
		return is_input


	def output(self):
		return self.measure_data()







		
		
