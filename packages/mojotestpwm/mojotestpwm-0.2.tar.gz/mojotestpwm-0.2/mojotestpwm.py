from machine import Pin, PWM, unique_id 
from umqtt.simple import MQTTClient

import ubinascii
import ujson
import time
import uasyncio as asyncio 



class Main:
	"""docstring for Main"""
	def __init__(self, pin=None, name = 'name'):
		super(Main, self).__init__()
		self.pin = pin 
		self.name = name 
		self.machine_id = ubinascii.hexlify(unique_id()).decode('utf-8')
		self.sub_client = MQTTClient(self.machine_id+'_'+self.name+'_sub', 'broker.hivemq.com')
		self.pub_client = MQTTClient(self.machine_id+'_'+self.name+'_pub', 'broker.hivemq.com')
		self.main()


	def _turn_off(self):

		#init the pwm pin with details
		pwm = PWM(Pin(self.pin, Pin.OUT))

		#deinit the pin in case its already running 
		pwm.deinit()


	def _process_msg(self, msg):

		#init the pwm pin with details
		pwm = PWM(Pin(self.pin, Pin.OUT))

		#deinit the pin in case its already running 
		pwm.deinit()

		msg_dict = eval(msg)

		#init the pin again and set it up as per the config provided by user. 

		try:
			pwm = PWM(Pin(self.pin, Pin.OUT), freq=msg_dict['freq'], duty=msg_dict['duty'])
			print(ujson.dumps({'success':1}))
			return ujson.dumps({'success':1, 'error':''})

		except Exception as e:
			print(ujson.dumps({'success':0, 'error':e}))
			return ujson.dumps({'success':0, 'error':e})



	#mqtt subscription callback.

	def sub_cb(self,topic, msg):
		#print(msg)
		#print(eval(msg))

		#return msg

		msg_dict = eval(msg)
		processed_msg = self._process_msg(msg)
		print(topic)
		#self.pub_client.connect()
		#self.pub_client.publish(topic, processed_msg)
		#self.pub_client.disconnect()
		print(processed_msg)

		"""if msg_dict['turn_off']==1:
			self._turn_off()
			self.pub_client.connect()

			self.pub_client.publish(topic, ujson.dumps({'success':1}))
			self.pub_client.disconnect()
			return ujson.dumps({'success':1})

		else:
			processed_msg = self._process_msg(msg)
			self.pub_client.connect()
			self.pub_client.publish(topic, processed_msg)
			self.pub_client.disconnect()
			return processed_msg"""

	def main(self):
		if not self.pin:
			return 'Pin not set'
		self.sub_client.set_callback(self.sub_cb)
		self.sub_client.connect()
		topic = self.machine_id+'/'+self.name
		self.sub_client.subscribe(topic)

		while True:
			if True:
				self.sub_client.wait_msg()
			else:
				self.sub_client.check_msg()
				#time.sleep(1)
				await uasyncio.sleep(1)


		self.sub_client.disconnect()











	












		

