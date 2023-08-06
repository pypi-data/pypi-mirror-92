from machine import Pin
from machine import unique_id
import ubinascii
from umqtt.simple import MQTTClient


import dht 
import time 
import ujson
import uasyncio as asyncio 



#test

class Main:
	"""docstring for ClassName"""
	def __init__(self, pin= None, type = 11, name = 'name'):

		self.pin = pin 
		self.is_output = True 
		self.is_input = False
		self.type = type 
		self.machine_id = ubinascii.hexlify(unique_id()).decode('utf-8')
		self.name = name 
		self.client = MQTTClient(self.machine_id+'_'+self.name, 'broker.hivemq.com')



	def measure_data(self):
		sensor_pin = Pin(self.pin, Pin.IN, Pin.PULL_UP)

		if self.type==11:

			
			
			sensor = dht.DHT11(sensor_pin)
			#time.sleep(3)
			await asyncio.sleep(3)
			try:
				sensor.measure()
				return ujson.dumps({'temperature':sensor.temperature(), 'humidity': sensor.humidity(), 'success':1, 'error':''})

			except Exception as e:
				return ujson.dumps({'temperature':0, 'humidity':0, 'success':0, 'error':e})
			
			
			

		else:

			sensor = dht.DHT22(sensor_pin)
			#time.sleep(3)
			await asyncio.sleep(3)
			try:
				sensor.measure()
				return ujson.dumps({'temperature':sensor.temperature(), 'humidity': sensor.humidity(), 'success':1, 'error':''})

			except:
				return ujson.dumps({'temperature':0, 'humidity':0, 'success':0, 'error':e})


	def main(self):
		if not self.pin:
			self.client.connect()
			data = ujson.dumps({'temperature':0, 'humidity':0, 'success':0, 'error':'Invalid Pin'})
			self.client.publish(self.machine_id+'/'+self.name, data)
			self.client.disconnect()
			return {'temperature':0, 'humidity':0, 'success':0, 'error':'Invalid Pin'}
		

		self.client.connect()

		while True:
			data = self.measure_data()
			self.client.publish(self.machine_id+'/'+self.name, data)
			


		self.client.disconnect()




			


	







		
		
