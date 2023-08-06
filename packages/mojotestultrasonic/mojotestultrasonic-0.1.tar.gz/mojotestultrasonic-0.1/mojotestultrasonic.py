from ultrasonic import HCSR04

from machine import Pin, unique_id

import time 

import ubinascii
from umqtt.simple import MQTTClient 
import ujson





class Main:
	"""docstring for Main"""
	def __init__(self, echo_pin=None, trigger_pin=None, name='name', echo_timeout_us=500*2*30):
		super(Main, self).__init__()
		self.echo_pin = echo_pin
		self.trigger_pin = trigger_pin
		self.name = name 
		self.echo_timeout_us = echo_timeout_us
		self.machine_id = ubinascii.hexlify(unique_id()).decode('utf-8')
		self.client = MQTTClient(self.machine_id+'_'+self.name, 'broker.hivemq.com')


	def _publish_error_message(self, error = ''):
		data = {'success':0, 'error':error, 'distance_cm':0, 'distance_mm':0}
		self.client.connect()
		topic = self.machine_id+'/'+self.name
		self.client.publish(topic, ujson.dumps(data))
		return ujson.dumps(data) 



	def measure_data(self):

		try:
			sensor = HCSR04(self.trigger_pin, self.echo_pin, echo_timeout_us= self.echo_timeout_us)
			data = {'success':1, 'error':'', 'distance_cm':sensor.distance_cm(), 'distance_mm':sensor.distance_mm()}
			return ujson.dumps(data)

		except Exception as e:
			data = {'success':0, 'error':e, 'distance_cm':0, 'distance_mm':0}
			return ujson.dumps(data)



	def main(self):
		if not self.echo_pin or not self.trigger_pin:
			self.client.connect()
			topic = self.machine_id+'/'+self.name
			self.client.publish(topic, ujson.dumps({'success':0, 'error':'pins not valid.', 'distance_cm':0, 'distance_mm':0}))
			return ujson.dumps({'success':0, 'error':'pins not valid.', 'distance_cm':0, 'distance_mm':0})

		self.client.connect()

		while True:
			topic = self.machine_id+'/'+self.name
			self.client.publish(topic, self.measure_data())

		self.client.disconnect()





		



